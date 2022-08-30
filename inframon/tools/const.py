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


"""String literals used in tools library.
   General constants are put in Consts class.
   There are different classes for different categories of literals used in the module.
"""


class Consts:
    """ General Category. """
    URL = 'url'
    # Below two can be removed once ConfManager is available
    USER = 'manage'
    PASS = 'Testit123!'
    SHOW = 'show'
    RESPONSE = 'response'
    NAME = 'name'
    LOCATION = 'location'
    LOCATION_STR = 'location_str'
    TYPE = 'type'
    SESSION_KEY = 'sessionKey'
    DATA_TYPE = 'datatype'
    JSON = 'json'
    URI_SET_ACK = '/api/set/alert/acknowledge/'
    URI_LOGIN = '/api/login/'
    URI_SHOW = '/api/show/'
    CHECKPOINT = 'checkpoint'
    STATUS = 'status'
    FAULT = 'fault'
    FAULT_RESOLVED = 'fault-resolved'
    ID = 'id'
    SUCCESS_CODE = 200
    FW_SLASH = '/'
    TIMESTAMP ='timestamp'
    UTF8 = 'utf-8'


class AlertConsts:
    """ String literal used by Enclosure Alerts. """
    NA = 'N/A'
    NAME = 'name'
    UNRESOLVED = 'unresolved'
    RESOLVED = 'resolved'
    DURABLE_ID = 'durable-id'
    SENSOR_STATUS = 'sensor-status'
    NW_PARAMS = 'network-parameters'
    SENSOR_NAME = 'sensor-name'
    CONTROLLER_ID = 'controller-id'
    OBJECT_NAME = 'object-name'
    RESPONSE = 'response'
    ALERTS = 'alerts'
    STATUS = 'status'
    REASON = 'reason'
    RECOMMENDED_ACTION = 'recommended-action'
    RESOLVED_NUM = 'resolved-numeric'
    RESPONSE_TYPE_NUM = 'response-type-numeric'
    DETECTED_TIME_NUM = 'detected-time-numeric'
    RESOLVED_TIME_NUM = 'resolved-time-numeric'
    ACK_NUM = 'acknowledged-numeric'
    REASON_NUM = 'reason-numeric'
    RECOMMENDED_ACTION_NUM = 'recommended-action-numeric'
    ID = 'id'
    SEVERITY = 'severity'
    COMPONENT = 'component'
    HEALTH = 'health'
    LOCATION = 'location'


class ResponseConsts:
    """ String literal used by response created by the tool module. """
    STATUS = 'status'
    RESOURCE = 'resource'
    RESOURCE_TYPE = 'resource_type'
    COMPONENT = 'component'
    RESOURCE_ID = 'resource_id'
    LOCATION = 'location'
    LOCATION_STR = 'location_str'
    DATA = 'data'
    HEALTH_STATUS = 'health_status'
    HEALTH_REASON = 'health_reason'
    HEALTH_RECOMMENDATION = 'health_recommendation'
    CODE = 'code'
    MESSAGE = 'message'
    DETECTED_TIME = 'detected_time'
    SPECIFIC_DATA = 'specific_data'
    ID = 'id'
    SEVERITY = 'severity'


class ErrorMessages:
    ENC_RESP_ERROR = 'Error in getting response from enclosure.'
    ALERT_ACK_ERROR = 'Cannot acknowledge alert with id = {alert_id}'
    CONT_CON_ERROR = 'Could not connect to controllers.'
    SESSION_ERROR = 'Session key not found.'
    RESP_BUILD_ERROR = 'No response builder found for type = {comp_type}'
