from abc import ABC, abstractmethod
import pymongo
from pymongo.errors import PyMongoError


class DB(ABC):
    @abstractmethod
    def get_data(self, **kwargs):
        pass

    @abstractmethod
    def save_data(self, data, **kwargs):
        pass


class MongoDB(DB):

    def __init__(self):
        # Initialize db connection
        # TODO : limit connection pool to max 10 connection.
        self._db = pymongo. \
            MongoClient("mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017/stream") \
            .get_database()

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
        except PyMongoError as e:
            print("An exception occurred. Error : ", e)
            # Log & Raise Exception

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

        except PyMongoError as e:
            print("An exception occurred. Error : ", e)
            # Log & Raise Exception


class MongoDBAdmin:

    def __init__(self) -> None:
        # Initialize db connection
        self._db = pymongo. \
            MongoClient("mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017/stream") \
            .get_database()

    def create_index(self, index_key, **kwargs):
        """
        Creates an index on this collection.
        Args:
            index_key (str): Name of index
        """

        bucket_name = kwargs.get('bucket_name')
        try:
            self._db[bucket_name].create_index(index_key)
        except PyMongoError as e:
            print("An exception occurred. Error : ", e)
            # Log & Raise Exception
