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

class Component(Resource):
    def __init__(self, resource_id: str, cmdcfg: CmdConfig, sitecfg: Config):
        if cmdcfg.get_resource_type(resource_id) == 'SERVER_NIC':
            resource_type = ResourceType.SERVER_NIC
        elif cmdcfg.get_resource_type(resource_id) == 'SERVER_HBA':
            resource_type = ResourceType.SERVER_HBA
        elif cmdcfg.get_resource_type(resource_id) == 'CLUSTER':
            resource_type = ResourceType.CLUSTER
        elif cmdcfg.get_resource_type(resource_id) == 'SOFTWARE':
            resource_type = ResourceType.SOFTWARE
        super().__init__(resource_type, resource_id, cmdcfg, sitecfg)

    def setup(self):
        ''' setup component using best practices '''
        setupPath = self.cmdcfg.get_resource_cmd(self.id, 'install_cmd')
        if setupPath:
            os.system("python3 %s" %setupPath)

    def configure(self):
        ''' configure component '''
        configPath = self.cmdcfg.get_resource_cmd(self.id, 'config_cmd')
        if configPath:
            os.system("python3 %s" %configPath)

    def validate(self):
        ''' validate resource setup and config '''
        validatePath = self.cmdcfg.get_resource_cmd(self.id, 'validate_cmd')
        if validatePath:
            os.system("python3 %s" %validatePath)

    def teardown(self):
        ''' teardown component'''
        teardownPath = self.cmdcfg.get_resource_cmd(self.id, 'teardown_cmd')
        if teardownPath:
            os.system("python3 %s" %teardownPath)

    def enable(self):
        ''' start / online component '''
        pass

    def disable(self):
        ''' stop / offline component'''
        pass

    def unconfigure(self):
        ''' configure component'''
        pass

    def upgrade(self):
        ''' upgrade resource using best practices '''
        pass

    def downgrade(self):
        ''' downgrade resource using best practices '''
        pass

