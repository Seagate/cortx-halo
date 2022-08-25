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
import logging

imagepath = "/opt/halo/install_depot/images"

def createDir():
    try:
        if os.system("ls %s" %(imagepath)) != 0:
            os.system("mkdir %s" %(imagepath))
            logging.getLogger("Directory Created %s" %imagepath)
    except Exception as e:
        logging.exception(f'{e}')

def loadImages():
    try:
        img = os.popen("ls %s/*.tar" %(imagepath)).read()
        imgList = img.split("\n")
        for i in imgList[:-1]:
            os.system("docker load < %s" %(i))
    except Exception as e:
        logging.exception(f'{e}')


def main():
    loadImages()


if __name__ == "__main__":
    main()