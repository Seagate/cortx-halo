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


""" This module implements tool for Enclosure APIs.
    Any communication to storage hardware happens via this code while using enclosure APIs.
"""


from abc import ABC, abstractmethod

import hashlib
import json
import threading
from typing import Any, List

import requests
from urllib3.exceptions import InsecureRequestWarning

from inframon.comps import StorageComponents
from inframon.tools.tool import Tool, ToolResponse
#from inframon.config import InfraMonConfig
from inframon.tools.const import Consts, AlertConsts, ResponseConsts, ErrorMessages
from inframon.utils import NoDirectCreator

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class EnclosureAPI(Tool):
    """ Implements Tools abstract class and provide get_status and describe methods to component monitors. """

    def __init__(self) -> None:
        self._api_connection = EnclosureAPIConnection.instance()
        self._location_map = {}
        self._sensor_type = {'_volt_': 'Voltage', '_temp_': 'Temperature', '_curr_': 'Current',
                       '_cap_capacitance_': 'Capacitor Capacitance',
                       '_cap_res_': 'Capacitor Resistance', '_cap_': 'Capacitor Charge'}
        # TODO: Improve building location map. Should be created just one time in the system.
        self.__initialize_location_map__()

    def __initialize_location_map__(self) -> None:
        """ Builds location map for every component by fetching information through /api/show endpoints.
            Since alerts do not have location information, the location map is built once when the object is
            created.
        """
        self._location_map = {}
        for a_component in StorageComponents.get_components_for_init():
            component_name = a_component[Consts.SHOW]
            response = self.get_status_raw(a_component)
            response = response[a_component[Consts.RESPONSE]]
            for an_element in response:
                if AlertConsts.DURABLE_ID in an_element:
                    entry = an_element[AlertConsts.DURABLE_ID]
                else:
                    entry = an_element[AlertConsts.NAME]

                if entry in self._location_map:
                    raise DuplicateComponentError(f"Duplicate = {entry}")

                self._location_map[entry] = {}
                self._location_map[entry][Consts.TYPE] = a_component[Consts.NAME]
                location = self._location_map[entry][Consts.LOCATION] = {}
                for a_location in a_component[Consts.LOCATION]:
                    if an_element[a_location] != AlertConsts.NA:
                        location[a_location] = an_element[a_location]

                if component_name == AlertConsts.SENSOR_STATUS:
                    # Relying on insertion order
                    for a_type in self._sensor_type:
                        if a_type in an_element[AlertConsts.DURABLE_ID]:
                            self._location_map[entry][Consts.TYPE] = self._sensor_type[a_type]
                            location[Consts.LOCATION_STR] = an_element[AlertConsts.SENSOR_NAME]
                            break
                elif component_name == AlertConsts.NW_PARAMS:
                    location[AlertConsts.CONTROLLER_ID] = an_element[AlertConsts.OBJECT_NAME]
                else:
                    if Consts.LOCATION in an_element:
                        location[Consts.LOCATION_STR] = an_element[AlertConsts.LOCATION]
                    else:
                        location[Consts.LOCATION_STR] = entry

    def get_status_raw(self, comp_type, **kwargs) -> Any:
        """ Provides raw output of /api/show endpoints """
        try:
            uri, session_key = self._api_connection.get_session_key()
            endpoint = EndpointBuilder.build(comp_type, **kwargs)
            uri += endpoint
            headers = {Consts.SESSION_KEY: session_key, Consts.DATA_TYPE: Consts.JSON}
            r = requests.get(uri, headers=headers, verify=False)
            response = json.loads(r.content)

            return response
        except EnclosureAPIError as exp:
            raise EnclosureAPIError(ErrorMessages.ENC_RESP_ERROR) from exp

    def get_status(self, comp_type, **kwargs) -> List[ToolResponse]:
        """ Gets the information from /api/show endpoints
            and converts the information to Json Response agreed with component monitor layer.
        """
        try:
            response = self.get_status_raw(comp_type, **kwargs)
            response = response[comp_type[Consts.RESPONSE]]
            result = ResponseBuilderFactory().get(comp_type[Consts.NAME]).build_response(response, **kwargs)
            to_delete = []
            for i, a_result in enumerate(result):
                resource_id = a_result.resource.resource_id
                if resource_id in self._location_map:
                    a_result.resource.location = self._location_map[resource_id]
                else:
                    # Remove these alerts for now. Add support later - supercap, system, snfs.
                    to_delete.append(i)
                    print(f"Error: Resource Id = {resource_id} not found.")

            for count, i in enumerate(to_delete):
                result.pop(i-count)

            return result
        except EnclosureAPIError as exp:
            raise EnclosureAPIError(ErrorMessages.ENC_RESP_ERROR) from exp

    def acknowledge(self, comp_type, alert_id) -> bool:
        """Acknowledges an alert. An acknowledged alert can be filtered out for
           identifying any new alert being generated in the system.
        """
        if comp_type[Consts.SHOW] == AlertConsts.ALERTS:
            try:
                uri, session_key = self._api_connection.get_session_key()
                uri += Consts.URI_SET_ACK + str(alert_id)
                headers = {Consts.SESSION_KEY: session_key, Consts.DATA_TYPE: Consts.JSON}
                r = requests.get(uri, headers=headers, verify=False)
                response = json.loads(r.content)
                if response[AlertConsts.STATUS][0][AlertConsts.RESPONSE_TYPE_NUM] != 0: # 200 ?
                    raise AcknowledgeAlertError(f"{ErrorMessages.ALERT_ACK_ERROR} {id}")
                return True
            except EnclosureAPIError as exp:
                raise EnclosureAPIError(ErrorMessages.ENC_RESP_ERROR) from exp
        else:
            pass

    def describe(self, comp_type, **kwargs):
        """Generate verbose information for every component in the enclosure.
        """


class EnclosureAPIConnection(metaclass=NoDirectCreator):
    """EnclosureAPIConnection is a Singleton class and used to store generated session key
       with a specific controller.
    """
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def reset_instance(cls, session_key) -> None:
        """Reset the connection, in case session key is expired
           and it needs to be generated again with same or other controller.
        """
        if cls.__singleton_instance:
            with cls.__singleton_lock:
                if cls.__singleton_instance and cls.__singleton_instance.get_session_key() == session_key:
                    cls.__singleton_instance = None

    @classmethod
    def instance(cls):
        """Gives the instance of the class."""
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls._create_instance()

        return cls.__singleton_instance

    def __init__(self) -> None:
        self._sessionKey = None
        self.__connect__()

    def __connect__(self) -> None:
        """Connects to enclosure by trying to different controllers.
           When succeeds, it stores controller information and session key.

        Enable this code later.
        conf_manager = InfraMonConfig.instance()
        user = conf_manager.get_config(EnclosureAPIConsts.USER)
        password = conf_manager.get_config(EnclosureAPIConsts.PASS)
        urls = conf_manager.get_config(EnclosureAPIConsts.URL)
        """

        user = Consts.USER
        password = Consts.PASS
        urls = ["https://10.0.0.2", "https://10.0.0.6"]
        num_connections = len(urls)

        auth_string = user + '_' + password
        auth_string = hashlib.sha256(auth_string.encode(Consts.UTF8)).hexdigest()
        for a_connection in range(1, num_connections+1):
            try:
                # Login and obtain the session key.
                headers = {Consts.DATA_TYPE: Consts.JSON}
                r = requests.get(urls[a_connection-1] + Consts.URI_LOGIN + auth_string, headers=headers, verify=False)
                if r.status_code == Consts.SUCCESS_CODE:
                    response = json.loads(r.content)
                    self._sessionKey = (urls[a_connection-1], response[AlertConsts.STATUS][0][AlertConsts.RESPONSE])
                else:
                    raise EnclosureAPIConnectionError(ErrorMessages.CONT_CON_ERROR)
            except Exception as exp:
                if a_connection == num_connections:
                    if isinstance(exp, EnclosureAPIConnectionError):
                        raise exp
                    else:
                        raise EnclosureAPIConnectionError(ErrorMessages.CONT_CON_ERROR) from exp
            else:
                break

    def get_session_key(self) -> tuple:
        """Return controller uri and session key."""
        if not self._sessionKey:
            raise EnclosureAPIConnectionError(ErrorMessages.SESSION_ERROR)

        return self._sessionKey


# Refactor this later, once there is more information.
class EndpointBuilder:
    """Builds uri for /api/show endpoints."""
    @staticmethod
    def build(comp_type, **kwargs) -> str:
        endpoint = Consts.URI_SHOW + comp_type[Consts.SHOW]
        if Consts.ID in kwargs:
            endpoint += Consts.FW_SLASH + kwargs[Consts.ID]
        if Consts.STATUS in kwargs:
            endpoint += Consts.FW_SLASH + kwargs[Consts.STATUS]

        return endpoint


class ResponseBuilder(ABC):
    """Different components have different outputs.
       The ResponseBuilder classes are used to parse the output and converts it to the
       response format understood by the upper modules.
    """
    @abstractmethod
    def build_response(self, response, **kwargs) -> List[ToolResponse]:
        pass


class ResponseBuilderFactory:
    """ A factory class for creating objects of
        different ResponseBuilder classes.
    """
    class_map = None
    key_attr = 'comp_type'

    @staticmethod
    def build_class_map() -> None:
        for _, an_entry in list(globals().items()):
            if an_entry is not ResponseBuilder and isinstance(an_entry, type) and issubclass(an_entry, ResponseBuilder):
                if hasattr(an_entry, ResponseBuilderFactory.key_attr):
                    ResponseBuilderFactory.class_map[getattr(an_entry, ResponseBuilderFactory.key_attr)] = an_entry

    @staticmethod
    def get(comp_type) -> ResponseBuilder:
        if ResponseBuilderFactory.class_map is None:
            ResponseBuilderFactory.class_map = {}
            ResponseBuilderFactory.build_class_map()

        if comp_type in ResponseBuilderFactory.class_map:
            return ResponseBuilderFactory.class_map[comp_type]()

        raise ResponseBuilderError(f"{ErrorMessages.RESP_BUILD_ERROR} {comp_type}.")


class AlertResponseBuilder(ResponseBuilder):
    """ ResponseBuilder class for alerts - /api/show/alerts
    """
    comp_type = StorageComponents.ALERT[Consts.NAME]

    @staticmethod
    def resolved_filter(timestamp, alert_id, record) -> bool:
        """ There is no definite way to track the already read resolved alerts.
            Only timestamp can be used.
        """
        if record[AlertConsts.RESOLVED_TIME_NUM] < timestamp:
            return False
        # There may be duplicate alerts sent to comm channel if multiple alerts are resolved at same time.
        elif record[AlertConsts.RESOLVED_TIME_NUM] == timestamp and record[AlertConsts.ID] == alert_id:
            return False

        return True

    @staticmethod
    def unresolved_filter(timestamp, alert_id, record) -> bool:
        """Any unresolved alert, when read by EnclosureAPI tool.
           So, every unresolved alert which is not acknowledged is a new
           alert generated in the system.
        """
        if record[AlertConsts.ACK_NUM] == 1:
            return False
        if record[AlertConsts.DETECTED_TIME_NUM] < timestamp:
            return False
        elif record[AlertConsts.DETECTED_TIME_NUM] == timestamp and record[AlertConsts.ID] <= alert_id:
            return False

        return True

    def build_response(self, response, **kwargs) -> List[ToolResponse]:
        filter_func = None
        if Consts.STATUS in kwargs and Consts.CHECKPOINT in kwargs:
            # Assuming checkpoint will be passed for resolved and unresolved only.
            if kwargs[Consts.STATUS] == AlertConsts.UNRESOLVED:
                filter_func = AlertResponseBuilder.unresolved_filter
            else:
                filter_func = AlertResponseBuilder.resolved_filter
        result = []
        for an_alert in response:
            if not filter_func or filter_func(kwargs[Consts.CHECKPOINT][Consts.TIMESTAMP], kwargs[Consts.CHECKPOINT][Consts.ID], an_alert):
                element = ToolResponse()
                if an_alert[AlertConsts.RESOLVED_NUM] == 0:
                    element.status = Consts.FAULT
                    element.data.specific_data[ResponseConsts.SEVERITY] = an_alert[AlertConsts.SEVERITY].upper()
                    element.data.detected_time = an_alert[AlertConsts.DETECTED_TIME_NUM]
                    element.data.health_reason.code = an_alert[AlertConsts.REASON_NUM]
                    element.data.health_reason.message = an_alert[AlertConsts.REASON]
                    element.data.health_recommendation.code = an_alert[AlertConsts.RECOMMENDED_ACTION_NUM]
                    element.data.health_recommendation.message = an_alert[AlertConsts.RECOMMENDED_ACTION]
                else:
                    element.status = Consts.FAULT_RESOLVED
                    element.data.detected_time = an_alert[AlertConsts.RESOLVED_TIME_NUM]

                element.data.specific_data[ResponseConsts.ID] = an_alert[AlertConsts.ID]
                element.resource.resource_id = an_alert[AlertConsts.COMPONENT]
                element.data.health_status = an_alert[AlertConsts.HEALTH].upper()

                result.append(element)

        return result


class EnclosureAPIError(Exception):
    pass


class DuplicateComponentError(EnclosureAPIError):
    pass


class EnclosureAPIConnectionError(EnclosureAPIError):
    pass


class ResponseBuilderError(EnclosureAPIError):
    pass


class AcknowledgeAlertError(EnclosureAPIError):
    pass

