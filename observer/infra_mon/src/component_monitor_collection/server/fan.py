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

# import pdb;pdb.set_trace()
# import sys, os

import const
from component_monitor_collection.component import Component
from tools.tool_factory import ToolFactory, ToolManager
from cortx.utils.log import Log
from event.event import Event


class Fan(Component):
    """Provides Fan component information and reports its status change"""

    NAME = "Fan"
    ELEMENT = const.SERVER

    def __init__(self):
        """Initialize component"""
        self.events = []
        self.tool_manager = ToolManager(self.ELEMENT, self.NAME)
        self.fan_list = self._get_component_list()
        Log.info(f"Initialized {self.ELEMENT} - {self.NAME} component monitor")

    def check_health_status(self):
        """
        Compare current health status with stored(previous) health status.
        If health status change in any of the identified fan modules is
        detected, create event on that specific fan module.
        """
        for fan_id in self.fan_list:
            fan_info = self.get_data(fan_id)
            stored_health = self._read_status_cache(self.ELEMENT, fan_id)
            current_health = self._get_health_status(fan_info)
            if not current_health:
                Log.error(f"Unable to fetch health status of {fan_id}")
                continue
            if current_health != stored_health:
                # Health status mismatch found
                Log.debug(f"{fan_id} - Health status is changed to {current_health}")
                event_msg = self._convert_to_event(fan_id, fan_info)
                if event_msg:
                    self.events.append(event_msg)

    def _get_component_list(self):
        """Get list of fan components"""
        comp_list = self.tool_manager.get_response(const.LIST, self.NAME)
        Log.debug(f"{self.NAME} list: {comp_list}")
        return comp_list

    def get_data(self, component_id):
        """
        Get component information
        Args:
            component_id - unique id of the fan module
        """
        data = self.tool_manager.get_response(const.GET, component_id)
        Log.debug(f"{component_id} data: {data}")
        if not data:
            Log.error(f"unable to fetch {component_id} information")
        return data

    def update_status_cache(self, element_type, component_id, status):
        """
        Update status cache if current health status is not matched
        with previous health status.
        Args:
            component_id - unique id of the fan module
            status - current health status
        """
        pass

    def _read_status_cache(self, element_type, fan_id):
        """
        When Status Cache get initialized, component status will be
        maintained with cloud_id, site_id, rack_id and node_id.
        Ex:
            fan_health_cid_sid_rid_nid.json
        """
        return ""

    def _get_health_status(self, info: dict):
        """
        Determine current health based on event type
        Args:
            info - unique id of the fan module
        """
        health = info.get("health", "NA")
        return health

    def _convert_to_event(self, resource_id: str, comp_info: dict, result: dict = {}):
        """
        Returns fields required for events.
        """
        event_type = ""
        event_severity = ""
        event = Event(self.ELEMENT, self.NAME, resource_id, event_type, event_severity, comp_info)
        return event.get_message()


if __name__ == "__main__":
    fan = Fan()
    fan.fan_list = ["Fan 1", "Fan 2"]
    fan.check_health_status()
    print(fan.events)
