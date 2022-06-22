# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

import inspect
import const
import importlib
from cortx.utils.log import Log


class ToolFactory:
    """Factory to provide instance of requested tool"""

    @staticmethod
    def get_tool(tool_name):
        module = importlib.import_module('tools')
        collection = inspect.getmembers(module, inspect.isclass)
        for kls_name, kls in collection:
             if tool_name.lower() == kls_name.lower():
                 return kls()
        return None


class ToolManager:
    """Routes the request to corresponding tool"""

    SERVER_NAME = "hpe"
    STORAGE_NAME = "corvault"

    def __init__(self, component):
        """Initialize tool manager"""
        self.component = component
        server_tools = const.COMPONENT_TOOL_MAPPING.get(self.SERVER_NAME)
        self.monitoring_tools = server_tools.get(self.component, [])
        self.component_name = self.component.split(":")[-1]

    def get_response(self, func=None, component_id=None):
        """
        Based on tool config (const.COMPONENT_TOOL_MAPPING),
        tool manager selects tool and returns response from the tool.
        """
        response = {}
        if not self.monitoring_tools:
            Log.error(f"No tool listed for monitoring '{self.component}'")
        for mon_tool in self.monitoring_tools:
            tool = ToolFactory.get_tool(mon_tool)
            response = tool.get_response(func, self.component_name, component_id)
            if response:
                break
        return response
