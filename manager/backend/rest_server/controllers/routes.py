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

from aiohttp import web
from manager import const
from manager.backend.rest_server.controllers.view import MgmtView

class MgmtRoutes():
    """
    Common class for adding routes
    """

    @staticmethod
    def add_routes(app):
        """
        Add routes to Web application
        """
        app.add_routes(MgmtView._app_routes)

    @staticmethod
    def add_websocket_routes(router, ws_handler):
        router.add_get("/ws", ws_handler)

class SwaggerRoutes:

    @staticmethod
    def _serve_swagger_ui(request):
       with open(const.SWAGGER_UI_INDEX_HTML, 'r') as f:
        return web.Response(text=f.read(), content_type='text/html')

    @staticmethod
    def _serve_swagger_json(request):
      with open(const.SWAGGER_JSON, 'r') as f:
        return web.Response(text=f.read(), content_type='application/json')

    @staticmethod
    def add_swagger_ui_routes(router):
      router.add_get(const.SWAGGER_UI_URL, SwaggerRoutes._serve_swagger_ui)
      router.add_get(const.SWAGGER_JSON_URL, SwaggerRoutes._serve_swagger_json)
      router.add_static(const.SWAGGER_UI_STATICS_URL, const.SWAGGER_UI_DIST)