import pymongo
from abc import ABC, abstractmethod
from common.db_store.error import DBError


class DB(ABC):
    @abstractmethod
    def get_data(self, **kwargs):
        pass

    @abstractmethod
    def save_data(self, data, **kwargs):
        pass


class MongoDB(DB):

    def __init__(self, endpoint, db_name, **kwargs) -> None:
        """Initialize DB connection.
        Args:
            endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            db_name (str): Name of database.
        """
        # TODO : Maintain maximum 10 connection in connection pool
        try:
            self._client = pymongo.MongoClient(endpoint)
            self._db = self._client[db_name]
        except Exception as e:
            # Log.error(f"Unable to connect database server endpoints \
            #     {endpoint} {e}")
            raise DBError(f"Unable to connect database server endpoints \
                {endpoint} with Error : {e}")

    def get_data(self, **kwargs):
        """
        Get list of documents that match the query criteria.

        Returns:
            result_list : List of document.
        """
        result_list = []

        bucket_name = kwargs.get('bucket_name')
        query_params = kwargs.get('queryparams')

        try:
            results = self._db[bucket_name].find(query_params)
            for result in results:
                result_list.append(result)
        except Exception as e:
            # Log.error(f"Unable to fetch data from data store. Error {e}")
            raise DBError(f"Unable to fetch data from data store. Error {e}")

        return result_list

    def save_data(self, data, **kwargs):
        """
        Save data to the collection.

        Args:
            data : JSON / BSON document to save to the collection.
        """
        bucket_name = kwargs.get('bucket_name')
        try:

            if '_id' in data:
                result = self._db[bucket_name]. \
                    replace_one({'_id': data['_id']}, data, upsert=True)
                return result.matched_count
            else:
                result = self._db[bucket_name].insert_one(data)
                return result.inserted_id

        except Exception as e:
            # Log.error(f"Unable to fetch data from data store. Error {e}")
            raise DBError(f"Unable to save data to data store. Error {e}")
