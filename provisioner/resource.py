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

from abc import ABC, abstractmethod
from const import ResourceType
from config import Config
from cmdconfig import *
import os

class Resource(ABC):

    def __init__(self, resource_type: ResourceType, resource_id: str, cmdcfg: CmdConfig, sitecfg: Config):
        self.type = resource_type
        self.id = resource_id
        self.cmdcfg = cmdcfg
        if sitecfg:
            self.sitecfg = sitecfg.get_resource_config(resource_type, resource_id)

    @abstractmethod
    def setup():
        ''' setup resource using best practices '''
        pass

    @abstractmethod
    def configure():
        ''' apply resource specific config from deployment_config '''
        pass

    @abstractmethod
    def enable():
        ''' turn resource online / available '''
        pass

    @abstractmethod
    def upgrade():
        ''' upgrade resource using best practices '''
        pass

    @abstractmethod
    def validate():
        ''' validate resource setup and config '''
        pass

    @abstractmethod
    def disable():
        ''' turn resource offline / unavailable '''
        pass

    @abstractmethod
    def downgrade():
        ''' downgrade resource using best practices '''
        pass

    @abstractmethod
    def unconfigure():
        ''' reset resource specific config applied '''
        pass

    @abstractmethod
    def teardown():
        ''' teardown resource setup '''
        pass

class Software(Resource):
    def __init__(self, resource_id: str, cmdcfg: CmdConfig, sitecfg: Config):
        super().__init__(ResourceType.SOFTWARE, resource_id, cmdcfg, sitecfg)
    def setup(self):
        ''' setup software using best practices '''
        setupPath = self.cmdcfg.config_dict[self.id]['install_cmd']
        os.system("python3 %s" %setupPath)
        print("hello")
    def configure(self):
        ''' configure software '''
        configPath = self.cmdcfg.config_dict[self.id]['config_cmd']
        os.system("python3 %s" %configPath)
    def validate(self):
        ''' validate resource setup and config '''
        validatePath = self.cmdcfg.config_dict[self.id]['validate_cmd']
        os.system("python3 %s" %validatePath)
    def teardown(self):
        ''' teardown software'''
        teardownPath = self.cmdcfg.config_dict[self.id]['teardown_cmd']
        os.system("python3 %s" %teardownPath)
    def enable(self):
        ''' start / online software '''
        pass
    def disable(self):
        ''' stop / offline software'''
        pass
    def unconfigure(self):
        ''' configure software'''
        pass
    def upgrade(self):
        ''' upgrade resource using best practices '''
        pass
    def downgrade(self):
        ''' downgrade resource using best practices '''
        pass
