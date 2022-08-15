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

import configparser
import collections
from const import FileType
from common.error import CustomError

class CmdConfig:
    def get_config_sections(self):
        try:
            section_dict = collections.defaultdict()
            for section in self.config.sections():
                section_dict[section] = dict(self.config.items(section))
            return section_dict
        except Exception as e:
            raise CustomError(f"Unable to parse config file. Error {e}")

    def __init__(self, file_type: FileType, config_file: str):
        try:
            self.file_type = file_type
            self.config_file = config_file
            self.config = configparser.RawConfigParser()
            self.config.read(self.config_file)
            self.config_dict = self.get_config_sections()
        except Exception as e:
            raise CustomError(f"Unable to Open config file. Error {e}")

if __name__ == "__main__":
    cfg = cfgparser(FileType.INI, './nodeprep.cfg')
    print(cfg.config_dict.keys())
    print(cfg.config_dict)

