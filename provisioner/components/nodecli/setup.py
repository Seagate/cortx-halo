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

import os

filename = "/opt/halo/install_depot/nodecli.tar.gz"
extract_path = "/opt/halo/install_depot/k8s"


def createFile():
    try:
        if os.system("ls %s" %(extract_path)) != 0:
            os.system("mkdir %s" %(extract_path))
            print("Directory Created %s" %extract_path)
    except Exception as e:
        print(f'{e}')


def setup():
    try:
        os.chdir("%s" %(extract_path))
        os.system("tar xvf %s -C %s" %(filename, extract_path))
        os.system("yum localinstall -y *.rpm")
    except Exception as e:
        print(f'{e}')


def main():
    createFile()
    setup()


if __name__ == "__main__":
    main()
