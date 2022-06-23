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

    def __init__(self):
        """Initialize component"""
        self.events = []
        self.element_type = const.SERVER
        self.tool_manager = ToolManager(self.element_type, self.NAME)
        Log.info(f"Initialized {self.element_type} - {self.NAME} component monitor")

    def check_health_status(self):
        """
        Compare current health status with stored(previous) health status.
        If health status change in any of the identified fan modules is
        detected, create event on that specific fan module.
        """
        fan_list = self.tool_manager.get_response(const.LIST, self.NAME)
        for fan_id in fan_list:
            info = self.get_info(fan_id)
            stored_health = self.read_cache(self.element_type, fan_id)
            current_health = self._get_current_health_status(info)
            if current_health != stored_health:
                # Health status mismatch found
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
        response = self.tool_manager.get_response(const.GET, component_id)
        if response:
            self._parse_data(response, info)
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

    def _get_current_health_status(self, info: dict):
        """
        Get current health
        Args:
            component_id - unique id of the fan module
        """
        health = info["health"]
        return health

    def convert_to_event(self, info):
        event = {}
        return event

