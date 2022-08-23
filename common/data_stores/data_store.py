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
from common.db_store.db_manager import DBManager
from const import DBTypes


class DocumentDataStore(ABC):

    def __init__(self, server_endpoint, db_name):
        self._server_endpoint = server_endpoint
        self._db_name = db_name

    @abstractmethod
    def get_data(self, **kwargs):
        pass

    @abstractmethod
    def store_data(self, data, **kwargs):
        pass

    @abstractmethod
    def delete_data(self, data, **kwargs):
        pass


class AlertStore(DocumentDataStore):

    def __init__(self, server_endpoint, db_name, data_store_name) -> None:
        super().__init__(server_endpoint, db_name)
        self._data_store_name = data_store_name
        # TODO: Read the db type from config file.
        self._dsb = DBManager.get_db_instance(
            db_type=DBTypes.MONGODB.value,
            db_endpoint=self._server_endpoint, db_name=self._db_name)

    def get_data(self, **kwargs):
        """Fetch data from store.

        Keyword Args:
            **kwargs: queryparams (json/bson): JSON / BSON string.

        Returns:
            list: List of records.
        """
        return self._dsb.get_data(self._data_store_name, **kwargs)

    def store_data(self, data, **kwargs):
        """Save data to store.

        Args:
            data (json/bson): JSON / BSON document to save to the data store.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JSON: {status: "", matched_count: "", insert_id: ""}
        """
        return self._dsb.save_data(self._data_store_name, data, **kwargs)

    def delete_data(self, data, **kwargs):
        """Delete data from store.

        Args:
            data (json/bson): JSON / BSON string.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            deleted count: 1 (Success) or 0 (Failure)
        """
        return self._dsb.delete_data(self._data_store_name, data, **kwargs)


class UserMgmtStore(DocumentDataStore):

    def __init__(self, server_endpoint, db_name, data_store_name) -> None:
        super().__init__(server_endpoint, db_name)
        self._data_store_name = data_store_name
        # TODO: Read the db type from config file.
        self._dsb = DBManager.get_db_instance(
            db_type=DBTypes.MONGODB.value,
            db_endpoint=self._server_endpoint, db_name=self._db_name)

    def get_data(self, **kwargs):
        """Fetch data from store.

        Keyword Args:
            **kwargs: queryparams (json/bson): JSON / BSON string.

        Returns:
            list: List of records.
        """
        return self._dsb.get_data(self._data_store_name, **kwargs)

    def store_data(self, data, **kwargs):
        """Save data to store.

        Args:
            data (json/bson): JSON / BSON document to save to the data store.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JSON: {status: "", matched_count: "", insert_id: ""}
        """
        return self._dsb.save_data(self._data_store_name, data, **kwargs)

    def delete_data(self, data, **kwargs):
        """Delete data from store.

        Args:
            data (json/bson): JSON / BSON string.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            deleted count: 1 (Success) or 0 (Failure)
        """
        return self._dsb.delete_data(self._data_store_name, data, **kwargs)
