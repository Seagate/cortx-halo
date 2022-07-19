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
import sys
import pathlib
import pytest
import argparse

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname
                                 (pathlib.Path(__file__)), '..'))

    default_path = os.path.join(os.path.dirname(pathlib.Path(__file__)), '..')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='path',
                        help='Any combination of directories,\
                        file names or node ids', default=default_path)
    parser.add_argument('-m', dest='marker',
                        help='Marker string for test group')
    args = parser.parse_args()

    args_list = ['-v']
    if args.marker:
        args_list.append('-m ' + args.marker)
    args_list.append(args.path)

    pytest.main(args_list)
