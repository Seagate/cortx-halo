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

class Resource(ABC):

    def __init__(self, resource_type: ResourceType, resource_id: str, cfg: Config):
        self.type = resource_type
        self.id = resource_id
        self.cfg = cfg.get_resource_config(resource_type, resource_id)

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


