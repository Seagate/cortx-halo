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

from enum import Enum
import pymongo
from abc import ABC, abstractmethod
from common.db_store.error import DBError


class DBAdmin(ABC):

    @abstractmethod
    def create_index(self, data_store_name, index_key, **kwargs):
        pass

    @abstractmethod
    def list_indexes(self, data_store_name, **kwargs):
        pass

    @abstractmethod
    def drop_index(self, data_store_name, index_name, **kwargs):
        pass

    @abstractmethod
    def open_connection(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def create_data_store(self, data_store_name, data_store_type, **kwargs):
        pass

    @abstractmethod
    def delete_data_store(self, data_store_name, data_store_type, **kwargs):
        pass

    @abstractmethod
    def get_data_stores(self):
        pass


class DATASTORE(Enum):
    TIMESERIES = "timeseries"
    ALERT = "alert"
    CONFIG = "config"
    PERF = "perf"


class MongoDBAdmin(DBAdmin):

    def __init__(self, endpoint: str, data_store_group: str) -> None:
        """Initialize Data store connection.

        Args:
            endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            data_store_group (str): Name of data store group.
        """
        self._endpoint = endpoint
        self._data_store_group = data_store_group
        self.open_connection()

    def open_connection(self):
        """Open data store connection.

        Raises:
            DBError: Unable to create connection.
        """
        try:
            self._client = pymongo.MongoClient(self._endpoint)
            self._data_group = self._client[self._data_store_group]
        except Exception as e:
            # TODO : Once logging enabled, uncomment all Log comments.
            # Log.error(f"Unable to connect data store server endpoints \
            #     {self._endpoint} {e}")
            raise DBError(f"Unable to connect data store server endpoints \
                          {self._endpoint} with Error : {e}")

    def create_index(self, data_store_name: str, index_key: str, **kwargs):
        """Create an index on this data store.

        Args:
            data_store_name (str): Name of data store.
            index_key (str): Key/field on which index is created.

        Raises:
            DBError: Unable to create index.
        """
        try:
            return self._data_group[data_store_name].create_index(index_key)
        except Exception as e:
            # Log.error(f"Unable to create Index. Error : {e}")
            raise DBError(f"Index '{index_key}' creation failed. {e}")

    def list_indexes(self, data_store_name: str, **kwargs):
        """List all index present in data store.

        Args:
            data_store_name (str): Name of data store.

        Returns:
            list: List of indexes.
        """
        index_list = []
        indexes = self._data_group[data_store_name].list_indexes()
        for index in indexes:
            index_list.append(index["name"])
        return index_list

    def drop_index(self, data_store_name: str, index_name: str, **kwargs):
        """Drop index from data store.

        Args:
            data_store_name (str): Name of data store.
            index_name (str): Index name.

        Raises:
            DBError: Unable to drop index.
        """
        if index_name in self.list_indexes(data_store_name):
            self._data_group[data_store_name].drop_index(index_name)
        else:
            raise DBError(f"Invalid index key {index_name}.")

    def close_connection(self):
        """End all server sessions created by current client \
            and disconnect from MongoDB."""
        self._client.close()

    def create_data_store(self, data_store_name: str,
                          data_store_type: str = None, **kwargs):
        """Create data store.

        Args:
            data_store (str): Type of data store.
            data_store_name (str): Name of data store.
            kwargs (_type_): keyword arguments.
        """
        if data_store_type == DATASTORE.TIMESERIES.value:
            timeField = kwargs.get('timeField')
            metaField = kwargs.get('metaField')
            granularity = kwargs.get('granularity')
            expire_time = kwargs.get('expire_time')
            try:
                if data_store_name not in self.get_data_stores():
                    return self._data_group.create_collection(
                        data_store_name,
                        timeseries={
                            'timeField': timeField,
                            'metaField': metaField,
                            'granularity': granularity},
                        expireAfterSeconds=expire_time)
                else:
                    return f"Data store {data_store_name} already exists."
            except Exception as e:
                # Log.error(f"Unable to create TimeSeries data_store \
                    # {data_store_name} Error : {e}")
                raise DBError(f"Unable to create Time Series data store \
                    {data_store_name}. Error : {e}")
        else:
            return self._data_group[data_store_name]

    def delete_data_store(self, data_store_name: str,
                          data_store_type: str = None, **kwargs):
        """Remove data store.

        Args:
            data_store_name (str): Name of data store.
            data_store_type (str): Type of data store.

        Raises:
            DBError: Invalid data store.
        """
        if data_store_name in self.get_data_stores():
            self._data_group.drop_collection(data_store_name)
        else:
            raise DBError(f"Invalid data store {data_store_name}.")

    def get_data_stores(self):
        """Get list of data stores."""
        return self._data_group.list_collection_names()
