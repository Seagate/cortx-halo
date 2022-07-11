import pymongo
from abc import ABC, abstractmethod
from common.db_store.error import DBError


class DBAdmin(ABC):

    @abstractmethod
    def create_index(self, collection, index_key, **kwargs):
        pass

    @abstractmethod
    def list_indexes(self, collection, **kwargs):
        pass

    @abstractmethod
    def drop_index(self, collection, index_name, **kwargs):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def create_timeseries_collection(self, collection, timeField, **kwargs):
        pass

    @abstractmethod
    def get_list_of_collections(self):
        pass


class MongoDBAdmin(DBAdmin):

    def __init__(self, endpoint: str, db_name: str, **kwargs) -> None:
        """Initialize DB connection.

        Args:
            endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            db_name (str): Name of database.

        Raises:
            DBError: Unable to connect.
        """
        try:
            self._client = pymongo.MongoClient(endpoint)
            self._db = self._client[db_name]
        except Exception as e:
            # Log.error(f"Unable to connect database server endpoints \
            #     {endpoint} {e}")
            raise DBError(f"Unable to connect database server endpoints \
                          {endpoint} with Error : {e}")

    def create_index(self, collection: str, index_key: str, **kwargs):
        """Create an index on this collection.

        Args:
            collection (str): Name of collection.
            index_key (str): Key/field on which index is created.

        Raises:
            DBError: Unable to create index.
        """
        try:
            return self._db[collection].create_index(index_key)
        except Exception as e:
            # Log.error(f"Unable to create Index. Error : {e}")
            raise DBError(f"Index '{index_key}' creation failed. {e}")

    def list_indexes(self, collection: str, **kwargs):
        """List all index present in collection.

        Args:
            collection (str): Name of collection.

        Returns:
            list: List of indexes.
        """
        index_list = []
        indexes = self._db[collection].list_indexes()
        for index in indexes:
            index_list.append(index["name"])
        return index_list

    def drop_index(self, collection: str, index_name: str, **kwargs):
        """Drop index from collection.

        Args:
            collection (str): Name of collection.
            index_name (str): Index name.

        Raises:
            DBError: Unable to drop index.
        """
        if index_name in self.list_indexes(collection):
            self._db[collection].drop_index(index_name)
        else:
            raise DBError(f"Invalid index key {index_name}.")

    def close_connection(self):
        """End all server sessions created by current client \
            and disconnect from MongoDB."""
        self._client.close()

    def create_timeseries_collection(self, collection: str,
                                 timeField: str, **kwargs):
        """Create Time series collection.

        Args:
            collection (str): Name of Collection.
            timeField (str): Field containing the timestamp.
            kwargs (_type_): Optional keyword arguments.

        Raises:
            DBError: Unable to create time series collection.
        """
        metaField = kwargs.get('metaField')
        granularity = kwargs.get('granularity')
        expire_time = kwargs.get('expire_time')
        try:
            if collection not in self._db.list_collections():
                return self._db.create_collection(
                    collection,
                    timeseries={
                        'timeField': timeField,
                        'metaField': metaField,
                        'granularity': granularity},
                    expireAfterSeconds=expire_time)
            else:
                return f"Collection {collection} already exists."
        except Exception as e:
            # Log.error(f"Unable to create TimeSeries collection {collection}\
            #     Error : {e}")
            raise DBError(f"Unable to create Time Series collection \
                {collection}. Error : {e}")

    def remove_collection(self, collection: str):
        """Remove collection from db store.

        Args:
            collection (str): Name of a collection to drop.

        Raises:
            DBError: Invalid collection.
        """
        if collection in self.get_list_of_collections():
            self._db.drop_collection(collection)
        else:
            raise DBError(f"Invalid collection {collection}.")

    def get_list_of_collections(self):
        """Get list of collections in db store."""
        return self._db.list_collection_names()
