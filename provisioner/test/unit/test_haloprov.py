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
from shutil import move, copyfile
from os import path
from haloprov import provision_components


pytestmark = pytest.mark.unit


def setup_config_file(srccfg, dest):
    restore = False
    origcfg = dest + srccfg
    if path.isfile(origcfg):
        origcfgbkup = origcfg + '.' + __name__
        move(origcfg, origcfgbkup)
        restore = True
    copyfile(srccfg, origcfg)
    return restore

def restore_config_file(dest, cfgfile):
    origcfg = dest + cfgfile
    origcfgbkup = origcfg + '.' + __name__
    if path.isfile(origcfgbkup):
        move(origcfgbkup, origcfg)
        return True
    return False

# Make sure that the test_network_config_output.yaml network specifications are applicable to test machine
# If any changes are made to network device names in test_network_config_output.yaml create expected output files
# Update the test_network_config_output.yaml for expected output files and actual output files paths
def test_haloprov():
    HALOPROV_PATH='/opt/seagate/halo/install_depot/config/'

    provcfg = 'haloprov.yaml'
    dest = HALOPROV_PATH
    restore_provcfg = setup_config_file(provcfg, dest)

    sitecfg = 'sitecfg.yaml'
    dest = HALOPROV_PATH
    restore_sitecfg = setup_config_file(sitecfg, dest)

    provision_components()

    if restore_provcfg:
        restore_config_file(dest, provcfg)

    if restore_sitecfg:
        restore_config_file(dest, sitecfg)

