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


import jinja2

def process(src_template_file, dest, data):
        templateLoader = jinja2.FileSystemLoader(searchpath="./jinja2_templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(src_template_file)
        network_config_data = template.render(data)
        try:
            if os.path.exists(dest):
                with open(dest, 'w') as fin:
                    fin.truncate()
                    fin.write(network_config_data)
        except Exception as e:
            print(e)

