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
    def open_connection(self, endpoint, data_store_group):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def create_data_store(self, data_store, data_store_name, **kwargs):
        pass

    @abstractmethod
    def delete_data_store(self, data_store_name):
        pass

    @abstractmethod
    def get_data_stores(self):
        pass


class DATASTORE(Enum):
    TIMESERIES = "timeseries"


class MongoDBAdmin(DBAdmin):

    def __init__(self, endpoint: str, data_store_group: str) -> None:
        """Initialize Data store connection.

        Args:
            endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            data_store_group (str): Name of data store group.
        """
        self._open_connection(endpoint, data_store_group)

    def _open_connection(self, endpoint: str, data_store_group: str):
        """Open data store connection.

        Args:
            endpoint (str): Data store endpoints.
            data_store_group (str): Name of data store group.

        Raises:
            DBError: Unable to create connection.
        """
        try:
            self._client = pymongo.MongoClient(endpoint)
            self._data_group = self._client[data_store_group]
        except Exception as e:
            # TODO : Once logging enabled, uncomment all Log comments.
            # Log.error(f"Unable to connect data store server endpoints \
            #     {endpoint} {e}")
            raise DBError(f"Unable to connect data store server endpoints \
                          {endpoint} with Error : {e}")

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

    def create_data_store(self, data_store: str,
                          data_store_name: str, **kwargs):
        """Create data store.

        Args:
            data_store (str): Type of data store.
            data_store_name (str): Name of data store.
            kwargs (_type_): keyword arguments.
        """
        if data_store == DATASTORE.TIMESERIES.value:
            metaField = kwargs.get('metaField')
            granularity = kwargs.get('granularity')
            expire_time = kwargs.get('expire_time')
            try:
                if data_store_name not in self.get_data_stores():
                    return self._data_group.create_collection(
                        data_store_name,
                        timeseries={
                            'timeField': data_store_name,
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
            self._data_group[data_store_name]

    def delete_data_store(self, data_store_name: str):
        """Remove data store.

        Args:
            data_store_name (str): Name of data store.

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
