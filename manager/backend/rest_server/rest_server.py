#!/usr/bin/env python3

# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing, please email
# opensource@seagate.com or cortx-questions@seagate.com.

import os
import errno
import asyncio
import json
import traceback
import signal
import ssl
import time
from abc import ABC
from weakref import WeakSet

from concurrent.futures import (CancelledError as ConcurrentCancelledError,
                                TimeoutError as ConcurrentTimeoutError)
from asyncio import CancelledError as AsyncioCancelledError
from aiohttp import web, web_exceptions
from aiohttp.client_exceptions import ServerDisconnectedError, ClientConnectorError, ClientOSError
from secure import SecureHeaders
from marshmallow import ValidationError, fields

from cortx.utils.errors import DataAccessError
from cortx.utils.log import Log

from manager import const
from manager.backend.errors import (MgmtError, MgmtNotFoundError, MgmtPermissionDenied,
                                    MgmtInvalidTokenError, MgmtExpiredTokenError,
                                    MgmtInternalError, InvalidRequest, ResourceExist,
                                    MgmtNotImplemented, MgmtServiceConflict, MgmtGatewayTimeout,
                                    MgmtRequestCancelled, MgmtUnauthorizedError, MGMT_UNKNOWN_ERROR,
                                    MGMT_HTTP_ERROR)
from manager.backend.rest_server.file_transfer import DownloadFileEntity
from manager.backend.rest_server.controllers.view import MgmtView, MgmtAccess, MgmtHttpException
from manager.backend.rest_server.controllers.routes import MgmtRoutes, SwaggerRoutes
from manager.backend.rest_server.controllers.validators import ValidateSchema
from manager.backend.user_manager.token_manager import MgmtTokenManager, validate_token

# ref: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
MGMT_BE_REST_DEFAULT_RATE_LIMIT = 5000

REST_PROTOCOL_HTTPS           = 'https'
REST_PROTOCOL_HTTP            = 'http'
MGMT_BE_REST_DEFAULT_PROTOCOL = REST_PROTOCOL_HTTP

MGMT_BE_REST_HTTP_PORT          = 7080
MGMT_BE_REST_HTTPS_PORT         = 7443
MGMT_BE_REST_DEFAULT_PORT  = MGMT_BE_REST_HTTP_PORT

MGMT_BE_SERVER_NAME      = 'mgmt_rest_server'
MGMT_BE_SERVER_LOG_PATH  = const.MGMT_PATH + '/logs/'
MGMT_BE_SERVER_LOG_LEVEL = 'INFO'


class ErrorResponseSchema(ValidateSchema):
    """
    Error Response validation schema
    """
    error_code = fields.Int(data_key=const.ERROR_CODE, required=True)
    message_id = fields.Str(data_key=const.MESSAGE_ID, required=True)
    message = fields.Str(data_key=const.MESSAGE_LITERAL, required=True)


class MgmtBeRestServer(ABC):
    """REST Interface to communicate with Management Backend."""

    enable_websocket = False
    __is_shutting_down = False
    __current_requests = 0
    __total_blocked = 0
    __rate_limit = 0

    # TODO : (CH-369) Add this in config data Store
    __token_sec = MgmtTokenManager.create_token_secret()

    @staticmethod
    def init(rate_limit=MGMT_BE_REST_DEFAULT_RATE_LIMIT, enable_websocket=False):
        """
        Initialize the

        Args:
            rate_limit (int, optional): REST API rate limit. Defaults to MGMT_BE_REST_DEFAULT_RATE_LIMIT.
            enable_websocket (bool, optional): True if websocket bg task to be used. Defaults to False.
        """

        MgmtBeRestServer.enable_websocket = enable_websocket
        if enable_websocket:
            MgmtBeRestServer._queue = asyncio.Queue()
            MgmtBeRestServer._background_tasks = []
            MgmtBeRestServer._ws_clients = WeakSet()

        MgmtBeRestServer.__rate_limit = rate_limit
        Log.info(f"Management Backend Server API rate limit is set to {MgmtBeRestServer.__rate_limit}")

        MgmtBeRestServer._app = web.Application(
            middlewares=[MgmtBeRestServer.throttler_middleware,
                         MgmtBeRestServer.set_secure_headers,
                         MgmtBeRestServer.rest_middleware,
                         MgmtBeRestServer.session_middleware,
                         MgmtBeRestServer.permission_middleware]
        )

        MgmtRoutes.add_routes(MgmtBeRestServer._app)

        # add websocket get handler
        if enable_websocket:
            MgmtRoutes.add_websocket_routes(
                MgmtBeRestServer._app.router, MgmtBeRestServer.process_websocket)

        SwaggerRoutes.add_swagger_ui_routes(MgmtBeRestServer._app.router)

        MgmtBeRestServer._app.on_response_prepare.append(MgmtBeRestServer._hide_headers)
        MgmtBeRestServer._app.on_startup.append(MgmtBeRestServer._on_startup)
        MgmtBeRestServer._app.on_shutdown.append(MgmtBeRestServer._on_shutdown)

    @staticmethod
    def is_debug(request) -> bool:
        """
        Check if request query contains debug keyword

        Args:
            request (aiohttp.Request): Client request object

        Returns:
            bool: True if request query contains debug keyword
        """
        return 'debug' in request.rel_url.query

    @staticmethod
    def error_response(err: Exception, **kwargs) -> dict:
        """
        Create a REST error response that to be returned to client

        Args:
            err (Exception): exception object

        Returns:
            dict: REST error response dict.
        """
        resp = {
            const.KEY_ERR_RESPONSE_ERROR_CODE: None,
            const.KEY_ERR_RESPONSE_MESSAGE_ID: None,
            const.KEY_ERR_RESPONSE_MESSAGE: None
        }

        request = kwargs.get("request")
        if MgmtBeRestServer.is_debug(request):
            resp[const.KEY_ERR_RESPONSE_STACKTRACE] = traceback.format_exc().splitlines()

        if isinstance(err, MgmtError):
            resp[const.KEY_ERR_RESPONSE_ERROR_CODE] = int(err.rc())
            resp[const.KEY_ERR_RESPONSE_MESSAGE_ID] = err.message_id()
            resp[const.KEY_ERR_RESPONSE_MESSAGE] = err.error()
            message_args = err.message_args()
            if message_args is not None:
                resp[const.KEY_ERR_RESPONSE_FORMAT_ARG] = err.message_args()
        elif isinstance(err, web_exceptions.HTTPError):
            resp[const.KEY_ERR_RESPONSE_ERROR_CODE] = MGMT_HTTP_ERROR
            resp[const.KEY_ERR_RESPONSE_MESSAGE_ID] = const.HTTP_ERROR
            resp[const.KEY_ERR_RESPONSE_MESSAGE] = str(err.reason)
        else:
            resp[const.KEY_ERR_RESPONSE_ERROR_CODE] = MGMT_UNKNOWN_ERROR
            resp[const.KEY_ERR_RESPONSE_MESSAGE_ID] = const.UNKNOWN_ERROR
            resp[const.KEY_ERR_RESPONSE_MESSAGE] = f'{str(err)}'

        try:
            # MGMT error response should have error_code message and message_id
            # Here we only check the Error response format
            # For incorrect format, only log the error
            schema = ErrorResponseSchema()
            err_response = schema.load(resp, unknown='EXCLUDE')
        except ValidationError as val_err:
            Log.error(f"Malformed error response format: {val_err}")

        return err_response

    @staticmethod
    def json_serializer(*args, **kwargs):
        """
        serialize to json string

        Args:
            args: arguments
            kwargs: keyword arguments
        Returns:
            str: json string
        """
        kwargs['default'] = str
        return json.dumps(*args, **kwargs)

    @staticmethod
    def json_response(response, status=const.STATUS_SUCCESS, response_headers=None):
        """
        Create web.json_response object and return

        Args:
            response (dict): response object
            status (int, optional): response status. Defaults to 200.
            response_headers (dict, optional): response headers. Defaults to None.

        Returns:
            web.json_response: json response that to sent to REST client.
        """
        return web.json_response(
            response, status=status, headers=response_headers, dumps=MgmtBeRestServer.json_serializer)

    @staticmethod
    def _raise_unauthorized_error(reason: str):
        """
        Security purpose raise common unauthorized error and suppress specific error.

        Args:
            reason (str): actual error message that to be suppressed.

        Raises:
            MgmtUnauthorizedError: _description_
        """
        Log.debug(f'Unauthorized: {reason}')
        raise MgmtUnauthorizedError(
            desc="Invalid authentication credentials or token for the target resource.")

    @staticmethod
    async def _resolve_handler(request):
        """
        from the request object get the handler function.

        Args:
             request (aiohttp.request): request object

        Returns:
            handler: handler function
        """
        match_info = await request.app.router.resolve(request)
        return match_info.handler

    @staticmethod
    async def _is_public(request):
        """
        Check whether handler function is public.

        Args:
            request (aiohttp.request): request object

        Returns:
            bool: True if public
        """
        path = request.url.path
        if path.startswith(const.SWAGGER_UI_URL) or path.startswith(const.SWAGGER_UI_STATICS_URL):
            return True
        handler = await MgmtBeRestServer._resolve_handler(request)
        return MgmtView.is_public(handler, request.method)

    @staticmethod
    async def _is_hybrid(request):
        """
        Check whether handler function is hybrid.
        note: hybrid can be configure to public or non public

        Args:
            request (aiohttp.request): request object

        Returns:
            bool: True if public
        """
        handler = await MgmtBeRestServer._resolve_handler(request)
        return MgmtView.is_hybrid(handler, request.method)

    @classmethod
    async def _get_permissions(cls, request):
        """
        Get required permissions of handler function

        Args:
            request (aiohttp.request): request object,
                for that required permissions to be fetched

        Returns:
            PermissionSet: required permission to serve request
        """
        handler = await MgmtBeRestServer._resolve_handler(request)
        return MgmtView.get_permissions(handler, request.method)

    @staticmethod
    @web.middleware
    async def throttler_middleware(request, handler):
        """
        throttle middleware: manage API rate limit and block the calls

        Args:
            request (aiohttp.request): request object
            handler (method): request handling method

        Returns:
            dict: response object
        """
        if MgmtBeRestServer.__current_requests >= MgmtBeRestServer.__rate_limit:
            # This block get executed when number of request reaches the request quota
            MgmtBeRestServer.__total_blocked += 1
            msg = (f"The request is blocked because the number of requests reached threshold\n"
                   f"Number of requests blocked since the start is {MgmtBeRestServer.__total_blocked}")
            Log.warn(msg)
            return web.Response(status=429, text="Too many requests")
        else:
            # This block get executed when number of request are less than request quota
            # Increment the counter for number of request executing
            MgmtBeRestServer.__current_requests += 1

        try:
            # Here we call handler
            # Handler can return json response or can raise an exception
            res = await handler(request)
        finally:
            # Decrements the counter of number of request executing
            # This block always gets executed
            MgmtBeRestServer.__current_requests -= 1
        return res

    @staticmethod
    @validate_token(secret=__token_sec)
    async def _call_non_public_handler(request, handler):
        """
        wrapper to validate token

        Args:
            request (aiohttp.request): request object
            handler (method): request handling method

        Returns:
            dict: response object
        """
        return await handler(request)

    @staticmethod
    @web.middleware
    async def session_middleware(request, handler):
        """
        Check whether the token is valid
        and check token session is expire and update it

        Args:
            request (aiohttp.request): request object
            handler (method): request handling method

        Returns:
            dict: response object
        """
        request.session = None
        is_public = await MgmtBeRestServer._is_public(request)
        is_hybrid = await MgmtBeRestServer._is_hybrid(request)
        if is_hybrid:
            # Note: The hybrid APIs are public by-default,
            # however can be configured to, either public or non-public.
            # In future if required hybrid APIs can be configured to non-public.
            # and then retrieve access info here.
            is_public = True

        Log.debug(f'{"Public" if is_public else "Non-public"}: {request}')
        try:
            if not is_public:
                return await MgmtBeRestServer._call_non_public_handler(request, handler)

        except (MgmtInvalidTokenError, MgmtExpiredTokenError) as e:
            MgmtBeRestServer._raise_unauthorized_error(e.error())
        return await handler(request)

    @classmethod
    @web.middleware
    async def permission_middleware(cls, request, handler):
        """
        Validate whether required permissions matches to the user permissions

        Args:
            request (aiohttp.request): request object
            handler (method): request handling method

        Raises:
            MgmtPermissionDenied: permission exception

        Returns:
            dict: response object
        """
        if request.session is not None:
            # Check whether user has required permissions.
            required = await cls._get_permissions(request)
            verdict = (request.session.permissions & required) == required
            Log.debug(f'Required permissions: {required}')
            Log.debug(f'User permissions: {request.session.permissions}')
            Log.debug(f'Allow access: {verdict}')
            if not verdict:
                Log.info(f"Authorization failed. User:"\
                f" {request.session.user_id}")
                raise MgmtPermissionDenied("Access to the requested resource"\
                    " is forbidden")
            Log.info(f"Authorization successful. User:"\
                f" {request.session.user_id}")
        return await handler(request)

    @staticmethod
    @web.middleware
    async def set_secure_headers(request, handler):
        """
        set secure header to obfuscate server information
        and to set Content-Security-Policy.

        Args:
            request (aiohttp.request): request object
            handler (method): request handling method

        Returns:
            dict: response body object
        """
        resp = await handler(request)
        SecureHeaders(csp=True, server=True).aiohttp(resp)
        return resp

    @staticmethod
    async def _remove_secret_values(request):
        """
        Remove keys and values for secret, password, and passwd from request object.

        Args:
            request (aiohttp.request): client request object
        """
        request_body = dict(request.rel_url.query) if request.rel_url.query else {}
        if not request_body and request.content_length and request.content_length > 0:
            try:
                request_body = await request.json()
            except Exception:
                request_body = {}
            if request_body:
                for key in list(request_body.keys()):
                    lower_key = key.lower()
                    if (lower_key.find("password") > -1 or lower_key.find("passwd") > -1 or
                        lower_key.find("secret") > -1):
                        del(request_body[key])

    @staticmethod
    def _fetch_bearer_token(request):
        """
        fetch updated token from session object.

        we will fetching the token from request.session
        but only non public function can have token exist and updated.
        So first we will be checking if token is exist and the fetch it.

        Args:
            request (aiohttp.request): client request object

        Returns:
            str: update token
        """
        updated_token = getattr(request.session, 'access_token', None)
        if updated_token:
            setattr(request.session, 'access_token', None)
            return f'{const.AUTH_TYPE} {updated_token}'

        return None

    @staticmethod
    async def _prepare_response(request, response):
        """
        Prepare response object to return to the client.

        Args:
            request (aiohttp.request): request object
            response (response): The response object
        Returns:
            web.Response: The Json response object to be return to the client
        """

        # fetch updated token in response header
        bearer_token = MgmtBeRestServer._fetch_bearer_token(request)

        if isinstance(response, DownloadFileEntity):
            file_response = web.FileResponse(response.path_to_file)
            file_response.headers[const.FILE_HEADER] = f'attachment; filename="{response.filename}"'
            if bearer_token:
                file_response.headers[const.AUTH_HEADER] = bearer_token
            return file_response

        if isinstance(response, web.StreamResponse) or isinstance(response, web.Response):
            if bearer_token:
                response.headers[const.AUTH_HEADER] = bearer_token
            return response

        return MgmtBeRestServer.json_response(response, status=const.STATUS_SUCCESS,
        response_headers={const.AUTH_HEADER: f'{const.AUTH_TYPE} {bearer_token}'} if bearer_token else None)

    @staticmethod
    async def _get_response_token_headers(request):
        """
        Create response headers to be return

        Args:
            request (aiohttp.request): request object

        Returns:
            dict: {'Authorization': 'Bearer <token>'}
        """
        bearer_token = MgmtBeRestServer._fetch_bearer_token(request)
        return {const.AUTH_HEADER: f'{const.AUTH_TYPE} {bearer_token}'} if bearer_token else None

    @staticmethod
    @web.middleware
    async def rest_middleware(request, handler):
        """
        REST middleware: Handling exception and creating response object.

        Args:
            request (aiohttp.request): request object
            handler (method): request handling method

        Raises:
            MgmtHttpException: raises to send it to REST client

        Returns:
            str: return JSON response object
        """
        if MgmtBeRestServer.__is_shutting_down:
            return MgmtBeRestServer.json_response("MGMT REST Server is shutting down", status=503)

        request_id = int(time.time())
        try:

            # remove keys and values for secret, password, and passwd from request object.
            await MgmtBeRestServer._remove_secret_values(request)

            response = await handler(request)

            return await MgmtBeRestServer._prepare_response(request, response)

        except (ConcurrentCancelledError, AsyncioCancelledError):
            Log.warn(f"Client cancelled call for {request.method} {request.path}")
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(
                    MgmtRequestCancelled(desc="Call cancelled by client"),
                    request=request, request_id=request_id),
                status=499, response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtHttpException as e:
            raise e
        except web.HTTPException as e:
            Log.error(f'HTTP Exception {e.status}: {e.reason}')
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id),
                status=e.status, response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except DataAccessError as e:
            Log.error(f"Failed to access the database: {e}")
            response = MgmtBeRestServer.error_response(e, request=request, request_id=request_id)
            return MgmtBeRestServer.json_response(response, status=503,
            response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except InvalidRequest as e:
            Log.debug(f"Invalid Request: {e} \n {traceback.format_exc()}")
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=400,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtNotFoundError as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=404,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtPermissionDenied as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=403,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except ResourceExist as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id),
                status=const.STATUS_CONFLICT, response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtInternalError as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=500,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtNotImplemented as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=501,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtGatewayTimeout as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=504,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtServiceConflict as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=409,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtUnauthorizedError as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=401,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except MgmtError as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=400,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except KeyError as e:
            Log.debug(f"Key Error: {e} \n {traceback.format_exc()}")
            message = f"Missing Key for {e}"
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(KeyError(message), request=request,
                                          request_id=request_id),
                status=422, response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except (ServerDisconnectedError, ClientConnectorError, ClientOSError,
                ConcurrentTimeoutError) as e:
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=503,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))
        except Exception as e:
            Log.critical(f"Unhandled Exception Caught: {e} \n {traceback.format_exc()}")
            return MgmtBeRestServer.json_response(
                MgmtBeRestServer.error_response(e, request=request, request_id=request_id), status=500,
                response_headers=MgmtBeRestServer._get_response_token_headers(request))

    @staticmethod
    async def _shut_down(loop, site, server=None):
        """
        operations to run before shut down

        Args:
            loop (AbstractEventLoop): asyncio event loop
            site (TCPSite): REST Server site
            server (AppRunner.Server, optional): Server object. Defaults to None.
        """
        MgmtBeRestServer.__is_shutting_down = True
        if server is not None:
            original_connections = server.connections.copy()
            for c in original_connections:
                while c in server.connections:
                    await asyncio.sleep(1)
        for task in asyncio.Task.all_tasks():
            if task != asyncio.Task.current_task():
                task.cancel()
        await site.stop()
        loop.stop()

    @staticmethod
    async def _hide_headers(request, response) -> None:
        del response.headers['Server']

    @staticmethod
    async def _handle_sigint(loop, site):
        Log.info('Received SIGINT, shutting down')
        await MgmtBeRestServer._shut_down(loop, site)

    @staticmethod
    async def _handle_sigterm(loop, site, server):
        Log.info('Received SIGTERM, shutting down')
        await MgmtBeRestServer._shut_down(loop, site, server)

    @staticmethod
    def _run_server(app, host=None, port=None, ssl_context=None, access_log=None):
        """
        Run the REST server

        Args:
            app (web.Application): REST Server application object
            host (str, optional): REST Server host. Defaults to None.
            port (int, optional): REST Server port number. Defaults to None.
            ssl_context (SSLContext, optional): ssl context. Defaults to None.
            access_log (Any, optional): access log object. Defaults to None.
        """
        loop = asyncio.get_event_loop()
        runner = web.AppRunner(app, access_log=access_log)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, host=host, port=port, ssl_context=ssl_context)
        loop.run_until_complete(site.start())
        handlers = {
            signal.SIGINT: lambda: MgmtBeRestServer._handle_sigint(loop, site),
            signal.SIGTERM: lambda: MgmtBeRestServer._handle_sigterm(loop, site, runner.server),
        }
        for k, v in handlers.items():
            loop.add_signal_handler(k, lambda v=v: asyncio.ensure_future(v())),
        print(f'======== MGMT REST Server is running on {site.name} ========')
        print('(Press CTRL+C to quit)', flush=True)
        try:
            loop.run_forever()
        finally:
            loop.close()

    @staticmethod
    def run(port = MGMT_BE_REST_DEFAULT_PORT,
            protocol = MGMT_BE_REST_DEFAULT_PROTOCOL,
            ssl_cert_path = None, ssl_key_path = None):
        """
        Run the REST server

        Args:
            port (int, optional): port number. Defaults to REST_BE_DEFAULT_PORT.
            protocol (str, optional): protocol 'HTTP' or HTTPS. Defaults to REST_BE_DEFAULT_PROTOCOL.
            ssl_cert_path (str, optional): SSL cert file path. Defaults to None.
            ssl_key_path (str, optional): SSL key file path. Defaults to None.

        Raises:
            MgmtError: Error if failed to run server with provided inputs
        """

        # Create SSL context if provided protocol is 'https'
        if protocol == REST_PROTOCOL_HTTPS:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            if not all(map(os.path.exists,
                           (ssl_cert_path,
                            ssl_key_path))):
                raise MgmtError(errno.ENOENT, "Invalid path to certificate/private key")
            ssl_context.load_cert_chain(ssl_cert_path, ssl_key_path)
        else:
            ssl_context = None
        MgmtBeRestServer._run_server(
            MgmtBeRestServer._app, port=port, ssl_context=ssl_context, access_log=None)

    @staticmethod
    async def _on_startup(app):
        """
        on startup function for application.
        This function will get called on startup of REST Server.

        Args:
            app (web.app): web app object
        """
        Log.debug('REST API startup')

    @staticmethod
    async def _on_shutdown(app):
        Log.debug('REST API shutdown')
        if MgmtBeRestServer.enable_websocket:
            for task in MgmtBeRestServer._background_tasks:
                task.cancel()

    @classmethod
    async def _ssl_cert_check_bg(cls):
        """
        Check SSL certificate in background task.
        """
        Log.debug('SSL certificate expiry check background task started')
        try:
            security_service = cls._app[const.SECURITY_SERVICE]
            await security_service.check_certificate_expiry_time_task()
        except AsyncioCancelledError:
            Log.debug('SSL certificate expiry check background task canceled')

        Log.debug('SSL certificate expiry check background task done')

    @staticmethod
    async def _async_push(msg):
        """
        async coroutine for

        Args:
            msg (_type_): _description_

        Returns:
            _type_: _description_
        """
        return await MgmtBeRestServer._queue.put(msg)

    @staticmethod
    def push(alert) -> bool:
        """
        Call asynchronous coroutine that pushes the alert in queue.
        this method can be called by system monitor to push alerts.

        Args:
            alert (str): Alert in JSON format that to be push to the client.

        Returns:
            bool : return True on success
        """
        push_coroutine = MgmtBeRestServer._async_push(alert)
        asyncio.run_coroutine_threadsafe(push_coroutine, MgmtBeRestServer._app.loop)
        return True

    @staticmethod
    def add_websocket_routes(router, ws_handler):
        """
        Add Web socket route to app router with GET handler function.

        Args:
            router (UrlDispatcher): application router
            ws_handler (function): GET handler function for websocket
        """
        router.add_get("/ws", ws_handler)

    @staticmethod
    @MgmtAccess.public
    async def process_websocket(request):
        """
        WebSocket Handle function for 'GET'.
        it Adds the websocket client

        Args:
            request (aiohttp.Request): received client request object

        Returns:
            WebSocketResponse: the websocket object.
        """
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        Log.debug('REST API websock connection opened')
        MgmtBeRestServer._ws_clients.add(ws)

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    Log.debug('REST API websock msg (ignored): %s' % msg)
                elif msg.type == web.WSMsgType.ERROR:
                    Log.debug('REST API websock exception: %s' % ws.exception())
            Log.debug('REST API websock connection closed')
            await ws.close()
        finally:
            MgmtBeRestServer._ws_clients.discard(ws)
        return ws

    @staticmethod
    async def add_wedsock_bg(app):
        """
        Add websocket background task which will be keep sending alter to websocket.

        Args:
            app (_type_): _description_
        """
        MgmtBeRestServer._background_tasks.append(app.loop.create_task(MgmtBeRestServer._websock_bg()))

    @staticmethod
    async def _websock_bg():
        """
        Function to execute as background function to broadcast new alerts
        """
        Log.debug('REST API websock background task started')
        try:
            while True:
                msg = await MgmtBeRestServer._queue.get()
                await MgmtBeRestServer._websock_broadcast(msg)
        except AsyncioCancelledError:
            Log.debug('REST API websock background task canceled')

        Log.debug('REST API websock background task done')

    @staticmethod
    async def _websock_broadcast(msg):
        # do explicit copy because the list can change asynchronously
        clients = MgmtBeRestServer._ws_clients.copy()
        try:
            for ws in clients:
                json_msg = MgmtBeRestServer.json_serializer(msg)
                await ws.send_str(json_msg)
        except Exception:
            Log.debug('REST API websock broadcast error')


if __name__ == '__main__':
    try:
        Log.init(MGMT_BE_SERVER_NAME,
                MGMT_BE_SERVER_LOG_PATH,
                MGMT_BE_SERVER_LOG_LEVEL,
                console_output=True,
                console_output_level='INFO')

        MgmtBeRestServer.init()
        MgmtBeRestServer.run()
    except Exception as e:
        Log.error(e)
        Log.error(traceback.format_exc())
        os._exit(1)
