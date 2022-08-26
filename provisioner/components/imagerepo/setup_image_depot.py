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
from provisioner.const import PATH


def createDir():
    try:
        if os.system("ls %s" %(PATH.IMAGE_TAR_FILE_PATH)) != 0:
            os.system("mkdir %s" %(PATH.IMAGE_TAR_FILE_PATH))
            print("Directory Created %s" %PATH.IMAGE_TAR_FILE_PATH) #TODO: Replace print with log
    except Exception as e:
        print(f'{e}') #TODO: Replace print with log

def loadImages():
    try:
        image_file = os.popen("ls %s*.tar" %(PATH.IMAGE_TAR_FILE_PATH)).read()
        img_list = image_file.split("\n")
        for img in img_list[:-1]:
            os.system("docker load < %s" %(img))
    except Exception as e:
        print(f'{e}') #TODO: Replace print with log


def main():
    loadImages()


if __name__ == "__main__":
    main()
