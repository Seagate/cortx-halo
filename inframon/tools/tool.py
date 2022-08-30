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


""" A Base class for implementing a Tool which
    interacts with the hardware or service to be monitored.
"""


from abc import ABC, abstractmethod

import json
import math
from typing import Any


class ResponseClassMarker(object):

    @staticmethod
    def format_dict(d) -> Any:
        p_d = {}
        # Assuming that only one level of dictionary will be used otherwise use the class.
        for a_key in d:
            if d[a_key] is None or (isinstance(d[a_key], str) and len(d[a_key]) == 0):
                continue
            p_d[a_key] = d[a_key]

        if len(p_d) == 0:
            return None

        return p_d

    def to_dict(self) -> Any:
        raw_dict = self.__dict__
        for k, v in raw_dict.items():
            if isinstance(v, ResponseClassMarker):
                raw_dict[k] = v.to_dict()
            elif isinstance(v, dict):
                raw_dict[k] = ResponseClassMarker.format_dict(v)
        processed_dict = {}
        for k, v in raw_dict.items():
            if v is not None:
                if isinstance(v, float) or (isinstance(v, str) and len(v) == 0):
                    continue
                processed_dict[k] = v
        if len(processed_dict) == 0:
            processed_dict = None
        return processed_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class ResourceType(ResponseClassMarker):
    def __init__(self) -> None:
        self.component: str = ''


class Resource(ResponseClassMarker):
    def __init__(self) -> None:
        self.resource_type: ResourceType = ResourceType()
        self.resource_id: str = ""
        self.location: dict = {}


class HealthInfo(ResponseClassMarker):
    def __init__(self) -> None:
        # Type hint is int but initialized to float, a placeholder to decide if missing.
        self.code: int = -math.inf
        self.message: str = ''


class ResponseData(ResponseClassMarker):
    def __init__(self) -> None:
        self.health_status: str = ''
        self.health_reason: HealthInfo = HealthInfo()
        self.health_recommendation: HealthInfo = HealthInfo()
        # Type hint is int but initialized to float, a placeholder to decide if missing.
        self.detected_time: int = -math.inf
        self.specific_data: dict = {}


class ToolResponse(ResponseClassMarker):
    def __init__(self) -> None:
        self.status: str = ""
        self.resource: Resource = Resource()
        self.data: ResponseData = ResponseData()


class Tool(ABC):
    @abstractmethod
    def get_status(self, comp_type, **kwargs) -> ToolResponse:
        pass

    @abstractmethod
    def describe(self, comp_type, **kwargs) -> ToolResponse:
        pass
