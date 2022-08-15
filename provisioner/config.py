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

import yaml, csv
import collections
from const import FileType, ResourceType

class Config:
    def __init__(self, file_type: FileType, config_file: str):
        self.file_type = file_type
        self.config_file = config_file
    def create_deployment_config(self) -> bool:
        ''' read input config (XLSX, site_survey_document.xlsx) into deployment_config yaml object '''
        self.resource_config = collections.defaultdict()
        return True
    def validate_deployment_config(self) -> bool:
        ''' validate deployment_config for expected configuration format and / or values '''
        return True
    def get_resource_config(self, resource_type: ResourceType, resource_id: str) -> dict:
        ''' read and return config json or yaml subset for given respurce type and id '''
        return self.resource_config

