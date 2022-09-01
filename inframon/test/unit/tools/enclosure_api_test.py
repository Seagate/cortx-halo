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


""" Only ResponseBuilder can be tested. For other classes, hardware is required.
"""

from inframon.tools.enclosure_api import ResponseBuilderFactory, AlertResponseBuilder
from inframon.comps import StorageComponents


resolved_alerts_input = [
    {'object-name': 'alerts', 'meta': '/meta/alerts', 'id': 1, 'component': 'mgmtport_b', 'serial-number': 'N/A',
     'description': 'Enclosure 0, Controller B, Network Port', 'durable-id': 'alert_mgmt_port.17',
     'condition-id': 'condition_mgmt_port.65', 'severity': 'INFORMATIONAL', 'severity-numeric': 0, 'resolved': 'Yes',
     'resolved-numeric': 1, 'acknowledged': 'No', 'acknowledged-numeric': 0, 'acknowledged-by': 'N/A',
     'acknowledged-time': 'N/A', 'acknowledged-time-numeric': 0, 'detected-time': '2021-07-12 15:35:38',
     'detected-time-numeric': 1626104138, 'resolved-time': '2021-08-04 17:58:12', 'resolved-time-numeric': 1628099892,
     'reminder-time': 'N/A', 'reminder-time-numeric': 0, 'hit-count': 2, 'basetype': 'mgmt_port', 'health': 'OK',
     'health-numeric': 0, 'reason': 'The network port health is unknown. It may be unhealthy.', 'reason-numeric': 6,
     'reason-id': 0,
     'recommended-action': '- Check in the event log for events related to this component and follow the recommended actions for those events.',
     'recommended-action-numeric': 1},
    {'object-name': 'alerts', 'meta': '/meta/alerts', 'id': 7, 'component': 'hostport_A0', 'serial-number': 'N/A',
     'description': 'Enclosure 0, Controller A, Host Port 0', 'durable-id': 'alert_host_port.01',
     'condition-id': 'condition_host_port.179', 'severity': 'INFORMATIONAL', 'severity-numeric': 0, 'resolved': 'Yes',
     'resolved-numeric': 1, 'acknowledged': 'No', 'acknowledged-numeric': 0, 'acknowledged-by': 'N/A',
     'acknowledged-time': 'N/A', 'acknowledged-time-numeric': 0, 'detected-time': '2022-08-23 07:14:03',
     'detected-time-numeric': 1661238843, 'resolved-time': '2022-08-23 07:17:24', 'resolved-time-numeric': 1661239044,
     'reminder-time': 'N/A', 'reminder-time-numeric': 0, 'hit-count': 5, 'basetype': 'host_port', 'health': 'OK',
     'health-numeric': 0, 'reason': 'There is no active connection to this host port.', 'reason-numeric': 11,
     'reason-id': 0,
     'recommended-action': '- If this host port is intentionally unused, no action is required.\n- Otherwise, use an appropriate interface cable to connect this host port to a switch or host.\n- If a cable is connected, check the cable and the switch or host for problems.',
     'recommended-action-numeric': 66},
    {'object-name': 'alerts', 'meta': '/meta/alerts', 'id': 8, 'component': 'controller_b',
     'serial-number': 'SGWUX210352FAC2', 'description': 'Enclosure 0, Controller B',
     'durable-id': 'alert_controller.19', 'condition-id': 'condition_controller.95', 'severity': 'CRITICAL',
     'severity-numeric': 3, 'resolved': 'Yes', 'resolved-numeric': 1, 'acknowledged': 'No', 'acknowledged-numeric': 0,
     'acknowledged-by': 'N/A', 'acknowledged-time': 'N/A', 'acknowledged-time-numeric': 0,
     'detected-time': '2021-12-30 16:47:38', 'detected-time-numeric': 1640882858,
     'resolved-time': '2021-12-30 16:48:36', 'resolved-time-numeric': 1640882916, 'reminder-time': 'N/A',
     'reminder-time-numeric': 0, 'hit-count': 3, 'basetype': 'controller', 'health': 'OK', 'health-numeric': 0,
     'reason': 'The controller is not operational.', 'reason-numeric': 24, 'reason-id': 0,
     'recommended-action': '- Restart the Storage Controller in this controller module, unless it is performing an operation where it is normal for it to be shut down, such as firmware update.',
     'recommended-action-numeric': 70}]

resolved_alerts_output = [
    {'data': {'detected_time': 1628099892, 'health_status': 'OK', 'specific_data': {'id': 1}},
     'resource': {'resource_id': 'mgmtport_b'}, 'status': 'fault-resolved'},
    {'data': {'detected_time': 1661239044, 'health_status': 'OK', 'specific_data': {'id': 7}},
     'resource': {'resource_id': 'hostport_A0'}, 'status': 'fault-resolved'},
    {'data': {'detected_time': 1640882916, 'health_status': 'OK', 'specific_data': {'id': 8}},
     'resource': {'resource_id': 'controller_b'}, 'status': 'fault-resolved'}]

resolved_alerts_output_cp = [
    {'data': {'detected_time': 1661239044, 'health_status': 'OK', 'specific_data': {'id': 7}},
     'resource': {'resource_id': 'hostport_A0'}, 'status': 'fault-resolved'}]

unresolved_alerts_input = [
    {'object-name': 'alerts', 'meta': '/meta/alerts', 'id': 6, 'component': 'disk_00.10',
     'serial-number': 'ZJV0AVS00000R8167ED6', 'description': 'Enclosure 0, Disk 10', 'durable-id': 'alert_disk.29',
     'condition-id': 'condition_disk.112', 'severity': 'WARNING', 'severity-numeric': 1, 'resolved': 'No',
     'resolved-numeric': 0, 'acknowledged': 'No', 'acknowledged-numeric': 0, 'acknowledged-by': 'N/A',
     'acknowledged-time': 'N/A', 'acknowledged-time-numeric': 0, 'detected-time': '2022-06-13 13:25:05',
     'detected-time-numeric': 1655126705, 'resolved-time': 'N/A', 'resolved-time-numeric': 0, 'reminder-time': 'N/A',
     'reminder-time-numeric': 0, 'hit-count': 1, 'basetype': 'disk', 'health': 'Degraded', 'health-numeric': 1,
     'reason': 'The disk has become leftover due to a timeout caused by disk degradation.', 'reason-numeric': 169,
     'reason-id': 0,
     'recommended-action': "- If the associated disk group is offline or quarantined, contact technical support. Otherwise, clear the disk's metadata to reuse the disk.",
     'recommended-action-numeric': 28},
    {'object-name': 'alerts', 'meta': '/meta/alerts', 'id': 19, 'component': 'hostport_A2', 'serial-number': 'N/A',
     'description': 'Enclosure 0, Controller A, Host Port 2', 'durable-id': 'alert_host_port.04',
     'condition-id': 'condition_host_port.03', 'severity': 'INFORMATIONAL', 'severity-numeric': 0, 'resolved': 'No',
     'resolved-numeric': 0, 'acknowledged': 'No', 'acknowledged-numeric': 0, 'acknowledged-by': 'N/A',
     'acknowledged-time': 'N/A', 'acknowledged-time-numeric': 0, 'detected-time': '2021-02-11 14:42:07',
     'detected-time-numeric': 1613054527, 'resolved-time': 'N/A', 'resolved-time-numeric': 0, 'reminder-time': 'N/A',
     'reminder-time-numeric': 0, 'hit-count': 1, 'basetype': 'host_port', 'health': 'OK', 'health-numeric': 0,
     'reason': 'There is no active connection to this host port.', 'reason-numeric': 11, 'reason-id': 0,
     'recommended-action': '- If this host port is intentionally unused, no action is required.\n- Otherwise, use an appropriate interface cable to connect this host port to a switch or host.\n- If a cable is connected, check the cable and the switch or host for problems.',
     'recommended-action-numeric': 66},
    {'object-name': 'alerts', 'meta': '/meta/alerts', 'id': 21, 'component': 'hostport_A3', 'serial-number': 'N/A',
     'description': 'Enclosure 0, Controller A, Host Port 3', 'durable-id': 'alert_host_port.06',
     'condition-id': 'condition_host_port.04', 'severity': 'INFORMATIONAL', 'severity-numeric': 0, 'resolved': 'No',
     'resolved-numeric': 0, 'acknowledged': 'No', 'acknowledged-numeric': 0, 'acknowledged-by': 'N/A',
     'acknowledged-time': 'N/A', 'acknowledged-time-numeric': 0, 'detected-time': '2021-02-11 14:42:08',
     'detected-time-numeric': 1613054528, 'resolved-time': 'N/A', 'resolved-time-numeric': 0, 'reminder-time': 'N/A',
     'reminder-time-numeric': 0, 'hit-count': 1, 'basetype': 'host_port', 'health': 'OK', 'health-numeric': 0,
     'reason': 'There is no active connection to this host port.', 'reason-numeric': 11, 'reason-id': 0,
     'recommended-action': '- If this host port is intentionally unused, no action is required.\n- Otherwise, use an appropriate interface cable to connect this host port to a switch or host.\n- If a cable is connected, check the cable and the switch or host for problems.',
     'recommended-action-numeric': 66}]

unresolved_alerts_output = [
    {'data': {'detected_time': 1655126705, 'health_reason': {'code': 169,
        'message': 'The disk has become leftover due to a timeout caused by disk degradation.'}, 'health_recommendation': {'code': 28,
        'message': "- If the associated disk group is offline or quarantined, contact technical support. Otherwise, clear the disk's metadata to reuse the disk."},
        'health_status': 'DEGRADED', 'specific_data': {'id': 6, 'severity': 'WARNING'}}, 'resource': {'resource_id': 'disk_00.10'}, 'status': 'fault'},
    {'data': {'detected_time': 1613054527, 'health_reason': {'code': 11,
        'message': 'There is no active connection to this host port.'}, 'health_recommendation': {'code': 66,
        'message': '- If this host port is intentionally unused, no action is required.\n- Otherwise, use an appropriate interface cable to connect this host port to a switch or host.\n- If a cable is connected, check the cable and the switch or host for problems.'},
        'health_status': 'OK', 'specific_data': {'id': 19, 'severity': 'INFORMATIONAL'}}, 'resource': {'resource_id': 'hostport_A2'},
        'status': 'fault'},
    {'data': {'detected_time': 1613054528, 'health_reason': {'code': 11,
        'message': 'There is no active connection to this host port.'}, 'health_recommendation': {'code': 66,
        'message': '- If this host port is intentionally unused, no action is required.\n- Otherwise, use an appropriate interface cable to connect this host port to a switch or host.\n- If a cable is connected, check the cable and the switch or host for problems.'},
        'health_status': 'OK', 'specific_data': {'id': 21, 'severity': 'INFORMATIONAL'}}, 'resource': {'resource_id': 'hostport_A3'},
        'status': 'fault'}]

unresolved_alerts_output_cp = [
    {'data': {'detected_time': 1655126705, 'health_reason': {'code': 169,
                                                             'message': 'The disk has become leftover due to a timeout caused by disk degradation.'}, 'health_recommendation': {'code': 28,
                                                                                                                                                                                'message': "- If the associated disk group is offline or quarantined, contact technical support. Otherwise, clear the disk's metadata to reuse the disk."},
              'health_status': 'DEGRADED', 'specific_data': {'id': 6, 'severity': 'WARNING'}}, 'resource': {'resource_id': 'disk_00.10'}, 'status': 'fault'},
    {'data': {'detected_time': 1613054528, 'health_reason': {'code': 11,
                                                             'message': 'There is no active connection to this host port.'}, 'health_recommendation': {'code': 66,
                                                                                                                                                       'message': '- If this host port is intentionally unused, no action is required.\n- Otherwise, use an appropriate interface cable to connect this host port to a switch or host.\n- If a cable is connected, check the cable and the switch or host for problems.'},
              'health_status': 'OK', 'specific_data': {'id': 21, 'severity': 'INFORMATIONAL'}}, 'resource': {'resource_id': 'hostport_A3'},
     'status': 'fault'}]


def test_alert_response_builder_object():
    """Test ResponseBuilderFactory."""
    res_builder = ResponseBuilderFactory.get(StorageComponents.ALERT['name'])
    assert isinstance(res_builder, AlertResponseBuilder), "Problem in creating Alert Response Builder Object."


def test_alert_resolved():
    """Test response created by AlertResponseBuilder for resolved alerts without checkpoint."""

    params = {'status': 'resolved'}
    result = ResponseBuilderFactory.get(StorageComponents.ALERT['name']).build_response(resolved_alerts_input, **params)
    result = [a_result.to_dict() for a_result in result]
    assert result == resolved_alerts_output, "Error in building response for resolved alerts with no checkpoint"


def test_alert_resolved_checkpoint():
    """Test response created by AlertResponseBuilder for resolved alerts with checkpoint."""

    params = {'status': 'resolved', 'checkpoint': {'timestamp': 1640882916, 'id': 8}}
    result = ResponseBuilderFactory.get(StorageComponents.ALERT['name']).build_response(resolved_alerts_input, **params)
    result = [a_result.to_dict() for a_result in result]
    assert result == resolved_alerts_output_cp, "Error in building response for resolved alerts with checkpoint"


def test_alert_unresolved():
    """Test response created by AlertResponseBuilder for unresolved alerts without checkpoint."""

    params = {'status': 'unresolved'}
    result = ResponseBuilderFactory.get(StorageComponents.ALERT['name']).build_response(unresolved_alerts_input, **params)
    result = [a_result.to_dict() for a_result in result]
    assert result == unresolved_alerts_output, "Error in building response for unresolved alerts with no checkpoint"


def test_alert_unresolved_checkpoint():
    """Test response created by AlertResponseBuilder for unresolved alerts with checkpoint."""

    params = {'status': 'unresolved', 'checkpoint': {'timestamp': 1613054527, 'id': 19}}
    result = ResponseBuilderFactory.get(StorageComponents.ALERT['name']).build_response(unresolved_alerts_input, **params)
    result = [a_result.to_dict() for a_result in result]
    assert result == unresolved_alerts_output_cp, "Error in building response for unresolved alerts with checkpoint"

