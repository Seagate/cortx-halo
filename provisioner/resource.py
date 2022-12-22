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
from const import ResourceType, PATH
from config import SiteConfig
from config import ResourcesConfig
import os
import yaml

class Resource(ABC):

    def __init__(self, resource_type: ResourceType, resource_id: str, rescfg: ResourcesConfig, siteconfig: SiteConfig):
        self.type = resource_type
        self.id = resource_id
        self.rescfg = rescfg
        self.rsccfg = None
        if siteconfig:
            self.rsccfg = siteconfig.get_resource_config(resource_type, resource_id)
            if self.rsccfg:
                rscfile = PATH.RESOURCE_CFGFILE.format(resource_id)
                if not os.path.isfile(rscfile):
                    basepath = os.path.dirname(__file__)
                    rscfile = basepath + '/' + rscfile
                with open(rscfile, 'w') as rsc:
                    yaml.dump(self.rsccfg, rsc)

    @abstractmethod
    def setup(self):
        ''' setup resource using best practices '''
        return

    @abstractmethod
    def configure(self):
        ''' apply resource specific config from deployment_config '''
        return

    @abstractmethod
    def enable(self):
        ''' turn resource online / available '''
        return

    @abstractmethod
    def upgrade(self):
        ''' upgrade resource using best practices '''
        return

    @abstractmethod
    def validate(self):
        ''' validate resource setup and config '''
        return

    @abstractmethod
    def disable(self):
        ''' turn resource offline / unavailable '''
        return

    @abstractmethod
    def downgrade(self):
        ''' downgrade resource using best practices '''
        return

    @abstractmethod
    def unconfigure(self):
        ''' reset resource specific config applied '''
        return

    @abstractmethod
    def teardown(self):
        ''' teardown resource setup '''
        return

class Component(Resource):
    def __init__(self, resource: str, rescfg: ResourcesConfig, siteconfig: SiteConfig):
        if rescfg.get_resource_type(resource) == 'SERVER_NIC':
            resource_type = ResourceType.SERVER_NIC
        elif rescfg.get_resource_type(resource) == 'SERVER_HBA':
            resource_type = ResourceType.SERVER_HBA
        elif rescfg.get_resource_type(resource) == 'CLUSTER':
            resource_type = ResourceType.CLUSTER
        elif rescfg.get_resource_type(resource) == 'SOFTWARE':
            resource_type = ResourceType.SOFTWARE
        resource_id = rescfg.get_resource_id(resource)
        super().__init__(resource_type, resource_id, rescfg, siteconfig)

    def setup(self):
        ''' setup component using best practices '''
        setupPath = self.rescfg.get_resource_cmd(self.id, 'install_cmd')
        if setupPath and os.path.isfile(setupPath):
            os.system("python3 %s" %setupPath)

    def configure(self):
        ''' configure component '''
        configPath = self.rescfg.get_resource_cmd(self.id, 'config_cmd')
        if configPath and os.path.isfile(configPath):
            os.system("python3 %s" %configPath)

    def validate(self):
        ''' validate resource setup and config '''
        validatePath = self.rescfg.get_resource_cmd(self.id, 'validate_cmd')
        if validatePath and os.path.isfile(validatePath):
            os.system("python3 %s" %validatePath)

    def teardown(self):
        ''' teardown component'''
        teardownPath = self.rescfg.get_resource_cmd(self.id, 'teardown_cmd')
        if teardownPath and os.path.isfile(teardownPath):
            os.system("python3 %s" %teardownPath)

    def enable(self):
        ''' start / online component '''
        return

    def disable(self):
        ''' stop / offline component'''
        return

    def unconfigure(self):
        ''' unconfigure component'''
        return

    def upgrade(self):
        ''' upgrade resource using best practices '''
        return

    def downgrade(self):
        ''' downgrade resource using best practices '''
        return

