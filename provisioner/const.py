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

from enum import Enum

class FileType(Enum):
    XLSX = 1
    CSV = 2
    INI = 3

class ResourceType(Enum):
    SERVER_NIC = 1
    SERVER_HBA = 2
    CLUSTER = 3
    SOFTWARE = 4

class SOFTWARE(Enum):
    ANSIBLE = 1
    NODECLI = 2
    K8S_CRI = 3
    
