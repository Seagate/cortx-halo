import pymongo
from abc import ABC, abstractmethod
from common.db_store.error import DBError


class DBAdmin(ABC):

    @abstractmethod
    def create_index(self, index_key, **kwargs):
        pass

    @abstractmethod
    def list_indexes(self, **kwargs):
        pass

    @abstractmethod
    def drop_index(self, index_name, **kwargs):
        pass

    @abstractmethod
    def close_connection(self):
        pass


class MongoDBAdmin(DBAdmin):

    def __init__(self, endpoint: str, db_name: str, **kwargs) -> None:
        """Initialize DB connection.
        Args:
            endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            db_name (str): Name of database.
        """
        try:
            self._client = pymongo.MongoClient(endpoint)
            self._db = self._client[db_name]
        except Exception as e:
            # Log.error(f"Unable to connect database server endpoints \
            #     {endpoint} {e}")
            raise DBError(f"Unable to connect database server endpoints \
                          {endpoint} with Error : {e}")

    def create_index(self, index_key: str, **kwargs):
        """Creates an index on this collection.
        Args:
            index_key (str): Key/field on which index is created.
        kwargs -
            bucket_name (str): Name of bucket.
        """
        bucket_name = kwargs.get('bucket_name')
        try:
            return self._db[bucket_name].create_index(index_key)
        except Exception as e:
            # Log.error(f"Unable to create Index. Error : {e}")
            raise DBError(f"Index '{index_key}' creation failed. {e}")

    def list_indexes(self, **kwargs):
        """List all index present in bucket.
        Keywords Args:
            bucket_name (str): Name of bucket
        Returns:
            List of indexes.
        """
        index_list = []
        bucket_name = kwargs.get('bucket_name')
        indexes = self._db[bucket_name].list_indexes()
        for index in indexes:
            index_list.append(index["name"])
        return index_list

    def drop_index(self, index_name: str, **kwargs):
        """Drop index from bucket.
        Args:
            index_name (str): Index name.
        Keywords Args:
            bucket_name (str): Name of bucket.
        """
        bucket_name = kwargs.get('bucket_name')
        if index_name in self.list_indexes(bucket_name):
            self._db[bucket_name].drop_index(index_name)
        else:
            raise DBError(f"Invalid index key {index_name}.")

    def close_connection(self):
        """End all server sessions created by current client \
            and disconnect from MongoDB."""
        self._client.close()

    def create_timeseries_bucket(self, bucket_name: str, **kwargs):
        """Create Time series bucket.
        Args:
            bucket_name (str): Name of bucket.
        Keyword Args:
            timeField : Field containing the timestamp. [ Required ]
            metaField : Meta information.[ Optional ]
            granularity: Default value 'seconds'
        """
        timesField = kwargs.get('timeField')
        metaField = kwargs.get('metaField')
        granularity = kwargs.get('granularity')
        try:
            if bucket_name not in self._db.list_collection_names():
                return self._db.create_collection(
                    bucket_name,
                    timeseries={
                        'timeField': timesField,
                        'metaField': metaField,
                        'granularity': granularity})
            else:
                return f"Bucket {bucket_name} already exists."
        except Exception as e:
            # Log.error(f"Unable to create Time Series bucket {bucket_name}.\
            #     Error : {e}")
            raise DBError(f"Unable to create Time Series bucket \
                {bucket_name}. Error : {e}")

    def remove_buckets(self, bucket_name: str):
        """Remove bucket from db store.
        Args:
            bucket_name (str): Name of a bucket to drop.
        """
        if bucket_name in self.get_list_of_bucket():
            self._db.drop_collection(bucket_name)
        else:
            raise DBError(f"Invalid bucket name {bucket_name}.")

    def get_list_of_bucket(self):
        """Get list of buckets in db store."""
        return self._db.list_collection_names()
