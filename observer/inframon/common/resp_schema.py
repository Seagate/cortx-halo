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

import json
import time
import const
import os


class RespSchema:

    __schema = None

    @staticmethod
    def get_schema():
        if not RespSchema.__schema:
            if not os.path.exists(const.EVENT_SCHEMA_FILE):
                raise FileNotFoundError(f"File not found.")
            with open(const.EVENT_SCHEMA_FILE) as schema:
                RespSchema.__schema = json.loads(schema.read())
        return RespSchema.__schema

    def _update_data(self):
        data = self._schema.get("data")

        data["health_status"] = self._comp_info.get(
            "health", data["health_status"])

        data["health_reason"]["code"] = self._comp_info.get(
            "health-reason-numeric", data["health_reason"]["code"])

        data["health_reason"]["message"] = self._comp_info.get(
            "health-reason", data["health_reason"]["message"])

        data["health_recommendation"]["code"] = self._comp_info.get(
            "health-recommendation-numeric", data["health_recommendation"]["code"])

        data["health_recommendation"]["message"] = self._comp_info.get(
            "health-recommendation", data["health_recommendation"]["message"])

    def _update_specific_data(self):
        specific_data = self._schema.get("data").get("specific_data", {})
        for attr, value in self._comp_info.items():
            if attr not in const.DEFAULT_HEALTH_ATTRIBUTES:
                specific_data.update({attr: value})

    def get_message(self):
        self._schema["version"] = self.VERSION
        self._schema["timestamp"] = int(time.time())
        self._schema["event_type"] = self._get_event_type()
        self._schema["event_severity"] = self._get_event_severity()
        self._schema["source"] = self.SOURCE
        self._schema["event_id"] = ""
        self._update_resource_info()
        self._update_data()
        self._update_specific_data()
        return json.dumps(self._schema)

    def _get_event_type(self):
        return self._comp_info["event_type"]

    def _get_event_severity(self):
        event_type_severity_map = {
            "insertion": "informational",
            "missing": "critical",
            "fault": "critical",
            "fault_resolved": "informational"
        }
        return event_type_severity_map[self._comp_info["event_type"]]


if __name__ == "__main__":
    element = ""
    component_name = ""
    resource_id = ""
    comp_info = {}
    event = Event(element, component_name, resource_id, comp_info)
    print(event.get_message())
