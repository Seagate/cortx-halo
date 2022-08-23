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
import os
from setup import test_setup
import yaml
import hashlib


pytestmark = pytest.mark.unit


# Make sure that the test_config.yaml network specifications are applicable to test machine
# If any changes are made to network device names in test_config.yaml create expected output files
# Update the test.cfg for expected output files and actual output files paths
def test_network_config():
    test_setup()
    with open("test.cfg", "r") as f:
        test_cfg = yaml.load(f, Loader=yaml.SafeLoader)
    for output_fn in test_cfg['expected_output_files']:
        date = ''
        with open(output_fn) as file_to_check:
            data = file_to_check.read()
            expected_md5 = hashlib.md5(str(data).encode('utf-8')).hexdigest()
        actual_output_fn = '/etc/sysconfig/network-scripts/' + output_fn
        date = ''
        with open(actual_output_fn) as file_to_check:
            data = file_to_check.read()
            actual_md5 = hashlib.md5(str(data).encode('utf-8')).hexdigest()
        if (expected_md5 != actual_md5):
            assert False, "Network configuration failed"
            break

