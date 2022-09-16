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

from os import path
from resource import Component
from config import ResourcesConfig, SiteConfig
from const import FileType, PATH

def main():
    basepath = path.dirname(__file__)
    node_cfgfile = PATH.NODEPREP_CFGFILE
    if not path.isfile(node_cfgfile):
        node_cfgfile = basepath + '/' + node_cfgfile
    site_cfgfile = PATH.SITE_CFGFILE
    if not path.isfile(site_cfgfile):
        site_cfgfile = basepath + '/' + site_cfgfile
    siteconfig = SiteConfig(FileType.YAML, site_cfgfile)
    nodeprovcfg = ResourcesConfig(FileType.YAML, node_cfgfile)
    resources = nodeprovcfg.get_resources()
    for resource in resources:
        comp = Component(resource, nodeprovcfg, siteconfig)
        if not comp.validate():
            comp.setup()
            comp.configure()
            comp.validate()


if __name__ == "__main__":
    main()

