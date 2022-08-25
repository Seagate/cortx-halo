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

import pytest
from provisioner.components.network.config import config
import yaml
import hashlib


pytestmark = pytest.mark.unit


# Make sure that the test_network_config_output.yaml network specifications are applicable to test machine
# If any changes are made to network device names in test_network_config_output.yaml create expected output files
# Update the test_network_config_output.yaml for expected output files and actual output files paths
def test_network_config():
    config(cfgfile='test_network_config_input.yaml')
    with open("test_network_config_output.yaml", "r") as f:
        test_cfg = yaml.load(f, Loader=yaml.SafeLoader)
    for output_fn in test_cfg['expected_output_files']:
        data = ''
        with open(output_fn) as file_to_check:
            data = file_to_check.read()
            expected_sha256 = hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        actual_output_fn = '/etc/sysconfig/network-scripts/' + output_fn
        data = ''
        with open(actual_output_fn) as file_to_check:
            data = file_to_check.read()
            actual_sha256 = hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        if (expected_sha256 != actual_sha256):
            assert False, "Network configuration failed"
            break

