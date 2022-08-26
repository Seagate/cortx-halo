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


from cortx.utils.errors import BaseError
from cortx.utils.log import Log
from manager.backend import const

MGMT_OPERATION_SUCCESSFUL = 0x0000
MGMT_ERR_INVALID_VALUE = 0x1001
MGMT_ERR_INTERRUPTED = 0x1002
MGMT_INVALID_REQUEST = 0x1003
MGMT_PROVIDER_NOT_AVAILABLE = 0x1004
MGMT_INTERNAL_ERROR = 0x1005
MGMT_SETUP_ERROR = 0x1006
MGMT_RESOURCE_EXIST = 0x1007
MGMT_OPERATION_NOT_PERMITTED = 0x1008
MGMT_FAILURE = 0x1009
MGMT_SERVICE_NOT_AVAILABLE = 0x100A
MGMT_REQUEST_CANCELLED = 0x100B
MGMT_NOT_IMPLEMENTED = 0x100C
MGMT_SERVICE_CONFLICT = 0x100D
MGMT_GATEWAY_TIMEOUT = 0x100E
MGMT_UNAUTHORIZED_ERROR = 0x100F
MGMT_UNKNOWN_ERROR = 0x1010
MGMT_HTTP_ERROR = 0x1011

S3_SERVICE_ERROR = 0x3000

class MgmtError(BaseError):
    """ Parent class for the cli error classes """

    status=400

    def __init__(self, rc=0, desc=None, message_id=None, message_args=None):
        """
        Instantiation Method for MgmtError class
        """
        super(MgmtError, self).__init__(rc=rc, desc=desc, message_id=message_id,
                                       message_args=message_args)
        # TODO: Log.error message will be changed when desc is removed and
        #  improved exception handling is implemented.
        # TODO: self._message_id will be formatted with self._message_args
        # Common error logging for all kind of MgmtError
        Log.error(f"{self._rc}:{self._desc}:{self._message_id}:{self._message_args}")


class MgmtSetupError(MgmtError):
    """
    This error will be raised when Manager setup is failed
    """
    _desc = "Manager setup failed."

    def __init__(self, _desc=None, message_id=const.SETUP_ERROR, message_args=None):
        """
        Instantiation Method for MgmtSetupError class
        """
        super(MgmtSetupError, self).__init__(
            MGMT_SETUP_ERROR, _desc, message_id, message_args)


class CommandTerminated(KeyboardInterrupt):
    """
    This error will be raised when some command is terminated during
    the processing
    """

    _err = MGMT_ERR_INTERRUPTED
    _desc = "Command is cancelled."

    def __init__(self, _desc=None):
        """
        Instantiation Method for CommandTerminated class
        """
        super(CommandTerminated, self).__init__(self._err, self._desc)


class InvalidRequest(MgmtError):
    """
    This error will be raised when an invalid response
    message is received for any of the cli commands.
    """

    _err = MGMT_INVALID_REQUEST
    _desc = "Invalid request."
    status=400

    def __init__(self, _desc=None, message_id=const.INVALID_REQUEST, message_args=None):
        """
        Instantiation Method for InvalidRequest class
        """
        super(InvalidRequest, self).__init__(
            MGMT_INVALID_REQUEST, _desc, message_id, message_args)


class ResourceExist(MgmtError):
    """
    This error will be raised when an resource already exist
    """

    _err = MGMT_RESOURCE_EXIST
    _desc = "Resource already exist."
    status=const.STATUS_CONFLICT

    def __init__(self, _desc=None, message_id=const.RESOURCE_EXISTS, message_args=None):
        """
        Instantiation Method for ResourceExist class
        """
        super(ResourceExist, self).__init__(
            MGMT_RESOURCE_EXIST, _desc, message_id, message_args)


class MgmtInvalidTokenError(MgmtError):
    """
    This error will be raised if request token is invalid
    """

    _err = MGMT_ERR_INVALID_VALUE
    _desc = "Invalid Token."

    def __init__(self, desc=None, message_id=const.INVALID_AUTH_ERROR, message_args=None):
        """
        Instantiation Method for MgmtInvalidTokenError class
        """
        super(MgmtInvalidTokenError, self).__init__(
            MGMT_ERR_INVALID_VALUE, 'Invalid Token error: %s' % desc,
            message_id, message_args)

class MgmtExpiredTokenError(MgmtError):
    """
    This error will be raised if request token is expired
    """

    _err = MGMT_ERR_INVALID_VALUE
    _desc = "Expired Token."

    def __init__(self, desc=None, message_id=const.EXPIRED_AUTH_ERROR, message_args=None):
        """
        Instantiation Method for MgmtExpiredTokenError class
        """
        super(MgmtExpiredTokenError, self).__init__(
            MGMT_ERR_INVALID_VALUE, 'Expired Token error: %s' % desc,
            message_id, message_args)

class MgmtInternalError(MgmtError):
    """
    This error is raised by CLI for all unknown internal errors
    """

    _desc = "Manager Internal Error."
    status=500

    def __init__(self, desc=None, message_id=const.INTERNAL_ERROR, message_args=None):
        """
        Instantiation Method for MgmtInternalError class
        """
        super(MgmtInternalError, self).__init__(
            MGMT_INTERNAL_ERROR, 'Internal error: %s' % desc,
            message_id, message_args)

class MgmtNotFoundError(MgmtError):
    """
    This error is raised for all cases when an entity was not found
    """

    _desc = "An entity was not found."
    status=404

    def __init__(self, desc=None, message_id=const.NOT_FOUND_ERROR, message_args=None):
        """
        Instantiation Method for MgmtNotFoundError class
        """
        super(MgmtNotFoundError, self).__init__(
            MGMT_INTERNAL_ERROR, desc,
            message_id, message_args)

class MgmtPermissionDenied(MgmtError):
    """
    This error is raised for all cases when we don't have permissions
    """

    _desc = "Access to the requested resource is forbidden."
    status=403

    def __init__(self, desc=None, message_id=const.PERMISSION_DENIED_ERROR, message_args=None):
        """
        Instantiation Method for MgmtPermissionDenied class
        """
        super(MgmtPermissionDenied, self).__init__(
            MGMT_OPERATION_NOT_PERMITTED, desc,
            message_id, message_args)


class MgmtResourceNotAvailable(MgmtInternalError):

    """Describes issues when requested resource is not available"""

    _desc = "Resource not available."

    def __init__(self, desc=None, message_id=const.RESOURCE_NOT_AVAILABLE, message_args=None):
        """
        Instantiation Method for MgmtResourceNotAvailable class
        """
        super(MgmtResourceNotAvailable, self).__init__(
            desc, message_id, message_args)


class MgmtTypeError(MgmtInternalError):

    """Issues related to incorrect type of argument/parameter, etc."""

    _desc = "Unsupported type."

    def __init__(self, desc=None, message_id=const.TYPE_ERROR, message_args=None):
        """
        Instantiation Method for MgmtTypeError class
        """
        super(MgmtTypeError, self).__init__(
            desc, message_id, message_args)


class MgmtNotImplemented(MgmtError):

    """This error represents HTTP 501 Not Implemented Error"""

    _desc = "Not Implemented."
    status=501

    def __init__(self, desc=None, message_id=const.NOT_IMPLEMENTED, message_args=None):
        """
        Instantiation Method for MgmtNotImplemented class
        """
        super(MgmtNotImplemented, self).__init__(
            MGMT_NOT_IMPLEMENTED, desc,
            message_id, message_args)


class MgmtServiceConflict(MgmtError):

    """Service in conflict stat or operation can cause that state"""

    _desc = "Service conflict state."
    status=409

    def __init__(self, desc=None, message_id=const.SERVICE_CONFLICT, message_args=None):
        """
        Instantiation Method for MgmtServiceConflict class
        """
        super(MgmtServiceConflict, self).__init__(
            MGMT_SERVICE_CONFLICT, desc,
            message_id, message_args)


class MgmtGatewayTimeout(MgmtError):

    """
    This error represents a scenario where Manager was acting as a gateway or proxy
    and did not receive a timely response from the upstream server.
    """

    _desc = "Unable to get timely response."
    status=504

    def __init__(self, desc=None, message_id=const.GATEWAY_TIMEOUT, message_args=None):
        """
        Instantiation Method for MgmtGatewayTimeout class
        """
        super(MgmtGatewayTimeout, self).__init__(
            MGMT_GATEWAY_TIMEOUT, desc,
            message_id, message_args)


class MgmtUnauthorizedError(MgmtError):

    """This error represents HTTP 401 Unauthorized Error"""

    _desc = "Invalid authentication credentials for the target resource."
    status=401

    def __init__(self, desc=None, message_id=const.UNAUTHORIZED_ERROR, message_args=None):
        """
        Instantiation Method for MgmtUnauthorizedError class
        """
        super(MgmtUnauthorizedError, self).__init__(
            MGMT_UNAUTHORIZED_ERROR, desc,
            message_id, message_args)


class MgmtServiceNotAvailable(MgmtError):

    """This error represents Manager service is Not Available."""

    _desc = "Manager service not available."

    def __init__(self, desc=None, message_id=const.SERVICE_NOT_AVAILABLE, message_args=None):
        """
        Instantiation Method for MgmtServiceNotAvailable class
        """
        super(MgmtServiceNotAvailable, self).__init__(
            MGMT_SERVICE_NOT_AVAILABLE, desc,
            message_id, message_args)


class MgmtRequestCancelled(MgmtError):
    """This error represents Manager service request is cancelled."""

    _desc = "Service request cancelled."

    def __init__(self, desc=None, message_id=const.REQUEST_CANCELLED, message_args=None):
        """
        Instantiation Method for MgmtRequestCancelled class
        """
        super(MgmtRequestCancelled, self).__init__(
            MGMT_REQUEST_CANCELLED, desc,
            message_id, message_args)
