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

from provisioner.components.network.const import NWCONSTS
import os
import jinja2
import yaml


def config(cfgfile = NWCONSTS.CONFIG_YAML):
    try:
        basepath = os.path.dirname(__file__)
        # Load ifcfg input
        if not os. path.isfile(cfgfile):
            cfgfile = basepath + '/' + cfgfile
        with open(cfgfile, "r") as f:
            ifcfg = yaml.load(f, Loader=yaml.SafeLoader)
        # Load static and dynamic ifcfg template files
        searchpath = basepath + '/' + NWCONSTS.JINJA_TMPL_PATH
        templateLoader = jinja2.FileSystemLoader(searchpath)
        templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True)
        static_ifcfg_template = templateEnv.get_template(NWCONSTS.STATIC_IFCFG_JINJA_TMPL)
        dynamic_ifcfg_template = templateEnv.get_template(NWCONSTS.DYNAMIC_IFCFG_JINJA_TMPL)
        # Iterate over interfaces to be configured in input config file
        for intf in ifcfg[NWCONSTS.INTERFACES_KEY].keys():
            # Activate the device connection via Network Manager
            os.system("nmcli device connect %s" %(ifcfg[NWCONSTS.INTERFACES_KEY][intf][NWCONSTS.INTERFACE_KEY]))
            # For every interface configuration input create required ifcfg file
            if ifcfg[NWCONSTS.INTERFACES_KEY][intf][NWCONSTS.BOOTPROTO_KEY] == NWCONSTS.DHCP:
                ifcfg_template = dynamic_ifcfg_template
            else:
                ifcfg_template = static_ifcfg_template
            # Render the template
            ifcfg_data = ifcfg_template.render(ifcfg[NWCONSTS.INTERFACES_KEY][intf])
            # Save the configuration to output file
            ifcfg_file = NWCONSTS.IFCFG_PFX + ifcfg[NWCONSTS.INTERFACES_KEY][intf][NWCONSTS.INTERFACE_KEY]
            ifcfg_file_final = NWCONSTS.IFCFG_PATH + '/' + ifcfg_file
            with open(ifcfg_file_final, "w") as f:
                f.write(ifcfg_data)
            print("Created {} File! -->".format(ifcfg_file_final))
            print(ifcfg_data)
            # Reapply the ifcfg-<interface> file created via Network Manager
            os.system("nmcli device reapply %s" %(ifcfg[NWCONSTS.INTERFACES_KEY][intf][NWCONSTS.INTERFACE_KEY]))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    config()

