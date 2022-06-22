#!/usr/bin/env python3

# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

import os
import sys
from setuptools import setup

# Get the installation dir
install_dir = "/opt/seagate/halo/infra/mon"

with open('README.md', 'r') as rf:
    long_description = rf.read()

def get_data_files() -> list:
    data_files = [(install_dir + '/meta-info', ['LICENSE', 'README.md'])]
    ignore_dirs = []
    replace_dirs_in_dest = ()
    conf_dir = 'conf'
    for root, _, file_names in os.walk(conf_dir):
        dest_root = root
        last_dir = root.split("/")[-1]
        if last_dir in ignore_dirs:
            continue
        if dest_root.endswith(replace_dirs_in_dest):
            dest_root = "/".join(dest_root.split("/")[:-1])
        # Repeat the check for double such sufixes
        if dest_root.endswith(replace_dirs_in_dest):
            dest_root = "/".join(dest_root.split("/")[:-1])
        dest_root = install_dir + '/' + dest_root
        src_files = []
        for a_file in file_names:
            src_files.append(root+"/"+a_file)
        if len(src_files) != 0:
            data_files.append((dest_root, src_files))
    # See if same dest_root multiple times create a problem
    return data_files

setup(name='infra_mon',
      version='0.0.1',
      url='https://github.com/Seagate/halo-mon',
      license='Seagate',
      author='Ajay Srivastava',
      author_email='ajay.srivastava@seagate.com',
      description='Component monitor for Halo',
      package_dir={'infra_mon': 'src'},
      packages=[
         'infra_mon.component_monitor_collection', 'infra_mon.tools'
      ],
      install_requires=[],
      package_data={
        'infra_mon': ['py.typed'],
      },
      data_files=get_data_files(),
      long_description=long_description,
      zip_safe=False,
      python_requires='>=3.6')