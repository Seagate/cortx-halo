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

from common.db_store.admin_db import MongoDBAdmin
from common.db_store.db import MongoDB


class DBManager:

    @staticmethod
    def get_db_instance(db_type, db_endpoint, db_name):
        """Factory method to return instance of DB.

        Args:
            db_type (str): Type of DB.
            db_endpoint (str): DB server endpoints.
            db_name (str): Name of DB.
        """
        factories = {
            "mongodb": MongoDB(db_endpoint=db_endpoint, db_name=db_name)
        }

        if db_type in factories:
            return factories[db_type]
        raise ValueError(db_type)

    @staticmethod
    def get_admin_db_instance(admin_db_type, db_endpoint, db_name):
        """Factory method to return instance of admin DB.

        Args:
            admin_db_type (str): Type of admin DB.
            db_endpoint (str): Admin DB server endpoints.
            db_name (str): Name of Admin DB.
        """
        factories = {
            "mongodb_admin": MongoDBAdmin(
                db_endpoint=db_endpoint, db_name=db_name)
        }

        if admin_db_type in factories:
            return factories[admin_db_type]
        raise ValueError(admin_db_type)
