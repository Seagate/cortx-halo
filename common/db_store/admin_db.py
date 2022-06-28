import pymongo
from abc import ABC, abstractmethod
from common.db_store.error import DBError


class DBAdmin(ABC):

    @abstractmethod
    def create_index(self, index_key, **kwargs):
        """
        Abstract method of DBAdmin
        """
        pass


class MongoDBAdmin(DBAdmin):

    def __init__(self, endpoint, db_name, **kwargs) -> None:
        """
        Initialize DB connection.

        Args:
            endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            db_name (str): Name of database.
        """

        server_endpoint = "/".join([endpoint, db_name])
        try:
            self._db = pymongo.MongoClient(server_endpoint).get_database()
        except Exception as e:
            # Log.error(f"Unable to connect database server endpoints \
            #     {server_endpoint} {e}")
            raise DBError(f"Unable to connect database server endpoints \
                          {server_endpoint} with Error : {e}")

    def create_index(self, **kwargs):
        """
        Creates an index on this collection.
        Args:
            index_key (str): Key/field on which index is created.
        """

        bucket_name = kwargs.get('bucket_name')
        index_key = kwargs.get('index_key')

        try:
            self._db[bucket_name].create_index(index_key)
        except Exception as e:
            # Log.error(f"Unable to create Index. Error : {e}")
            raise DBError(f"Index creation failed. {e}")
