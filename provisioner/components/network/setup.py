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

#!/usr/bin/env python3

import os
import jinja2
import yaml

def setup():
    try:
        # Load ifcfg input
        with open("config.yaml", "r") as f:
            ifcfg = yaml.load(f, Loader=yaml.SafeLoader)
        # Load static and dynamic ifcfg template files
        with open("static_ifcfg.j2", "r") as f:
            static_ifcfg_template = jinja2.Template(f.read())
        with open("dynamic_ifcfg.j2", "r") as f:
            dynamic_ifcfg_template = jinja2.Template(f.read())

        for intf in ifcfg['interfaces'].keys():
            # Activate the device connection via Network Manager
            os.system("nmcli device connect %s" %(ifcfg['interfaces'][intf]['interface']))
            # For every interface configuration input create required ifcfg file
            if ifcfg['interfaces'][intf]['bootproto'] == 'dhcp':
                ifcfg_template = dynamic_ifcfg_template
            else:
                ifcfg_template = static_ifcfg_template
            # Render the template
            ifcfg_data = ifcfg_template.render(ifcfg['interfaces'][intf])
            # Save the configuration to output file
            ifcfg_file = "ifcfg-" + ifcfg['interfaces'][intf]['interface']
            ifcfg_file_final = '/etc/sysconfig/network-scripts/' + ifcfg_file
            with open(ifcfg_file_final, "w") as f:
                f.write(ifcfg_data)
            print("Created {} File! -->".format(ifcfg_file_final))
            print(ifcfg_data)
            # Reapply the ifcfg-<interface> file created via Network Manager
            os.system("nmcli device reapply %s" %(ifcfg['interfaces'][intf]['interface']))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    setup()

