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

import const
from component import Component
from tools.tool_factory import ToolFactory, ToolManager
from cortx.utils.log import Log


class Fan(Component):
    """Provides Fan component information and reports its status change"""

    NAME = "Fan"
    COMPONENT_TYPE = "server:fan"

    def __init__(self):
        """Initialize component"""
        self.events = []
        self.tool_manager = ToolManager(self.COMPONENT_TYPE)
        Log.info(f"Initialized {self.NAME} component monitor")

    def check_health_status(self):
        """
        Compare current health status with stored(previous) health status.
        If health status change in any of the identified fan modules is
        detected, create event on that specific fan module.
        """
        fan_list = self.tool_manager.get_response("list", self.NAME)
        for fan_id in fan_list:
            info = self.get_info(fan_id)
            stored_health_status = self.read_cache(self.COMPONENT_TYPE, fan_id)
            current_health_status = self._get_current_health(fan_id)
            if stored_health_status != current_health_status:
                event = self.convert_to_event(info)
                if event:
                    self.events.append(event)

    def get_info(self, component_id=None):
        """
        Get component health information
        Args:
            component_id - unique id of the fan module
        """
        info = {}
        response = self.tool_manager.get_response("get", component_id)
        if response:
            self._parse_response(response, info)
        return info

    def _update_status_cache(self, component_id, status):
        """
        Update status cache if current health status is not matched
        with previous health status.
        Args:
            component_id - unique id of the fan module
            status - current health status
        """
        pass

    def _get_current_health(self, component_id: str):
        """
        Get current health
        Args:
            component_id - unique id of the fan module
        """
        data = self.get_info(component_id)
        return data["status"]

    def _parse_response(self, data: dict, result: dict):
        """
        Parse dict type message and add only required field for event creation
        Args:
            data - contains raw information about the component(unformatted)
            result - event required fields will be added to result
        """
        return result

    def convert_to_event(self, info):
        event = {}
        return event

