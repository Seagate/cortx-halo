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


""" This contains classes for listing down components in different hardware.
    In the code, the component should be referred using classes defined in here.
"""


class StorageComponents:
    """ Components for Storage Enclosure """
    ALERT = {'name': 'Alert', 'response': 'alerts', 'show': 'alerts', 'location': []}
    ENCLOSURE = {'name': 'Enclosure', 'response': 'enclosures', 'show': 'enclosures', 'location': []}
    CONTROLLER = {'name': 'Controller', 'response': 'controllers', 'show': 'controllers', 'location': []}
    DISK_GROUP = {'name': 'Disk Group', 'response': 'disk-groups', 'show': 'disk-groups', 'location': ['pool']}
    DISK = {'name': 'Disk', 'response': 'drives', 'show': 'disks',
            'location': ['enclosure-id', 'drawer-id', 'slot', 'disk-group', 'storage-pool-name']}
    FAN_MODULE = {'name': 'Fan Module', 'response': 'fan-modules', 'show': 'fan-modules',
                  'location': ['enclosure-id', 'dom-id']}
    FAN = {'name': 'Fan', 'response': 'fan', 'show': 'fans', 'location': []}
    POOL = {'name': 'Pool', 'response': 'pools', 'show': 'pools', 'location': []}
    PORT = {'name': 'Port', 'response': 'port', 'show': 'ports', 'location': ['controller']}
    NETWORK = {'name': 'Mgmt Port', 'response': 'network-parameters', 'show': 'network-parameters', 'location': []}  # controller from object-name
    PSU = {'name': 'Power Supply', 'response': 'power-supplies', 'show': 'power-supplies',
           'location': ['enclosure-id', 'dom-id', 'position']}
    SAS_LINK = {'name': 'Sas Link', 'response': 'expander-ports', 'show': 'sas-link-health', 'location': []}  # didn't get any output. Handle it later
    VOLUME = {'name': 'Volume', 'response': 'volumes', 'show': 'volumes',
              'location': ['virtual-disk-name', 'storage-pool-name']}
    SENSOR = {'name': 'Sensor', 'response': 'sensors', 'show': 'sensor-status',
              'location': ['enclosure-id', 'controller-id']}  # resource type from container.

    """"Analyze and add later
    HOST_GROUP = {'show': 'host-groups', 'location': []}
    HOST_PHY
    HOST_PORT
    """

    @staticmethod
    def get_components_for_init():
        return [StorageComponents.ENCLOSURE, StorageComponents.CONTROLLER, StorageComponents.DISK,
                StorageComponents.DISK_GROUP, StorageComponents.FAN_MODULE, StorageComponents.FAN,
                StorageComponents.PORT, StorageComponents.NETWORK, StorageComponents.PSU,
                StorageComponents.SAS_LINK, StorageComponents.VOLUME, StorageComponents.SENSOR]


class ServerComponents:
    """ Components for Server Machine """
    pass
