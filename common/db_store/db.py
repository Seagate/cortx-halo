from enum import Enum
import pymongo
from abc import ABC, abstractmethod
from common.db_store.error import DBError


class DB(ABC):
    @abstractmethod
    def get_data(self, collection, **kwargs):
        pass

    @abstractmethod
    def save_data(self, collection, data, **kwargs):
        pass


class STATUSES(Enum):
    SUCCESS = "success"


class MongoDB(DB):

    def __init__(self, endpoint, db_name, **kwargs) -> None:
        """
        Initialize DB connection.
        Args:
            endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            db_name (str): Name of Database.
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

    def get_data(self, collection: str, **kwargs):
        """
        Get list of documents that match the query criteria.
        Args -
            collection (str): Name of collection.
        Returns:
            result_list : List of document.
        """
        result_list = []
        query_params = kwargs.get('queryparams')

        try:
            results = self._db[collection].find(query_params)
            for result in results:
                result_list.append(result)
        except Exception as e:
            # Log.error(f"Unable to fetch data from data store. Error {e}")
            raise DBError(f"Unable to fetch data from data store. Error {e}")

        return result_list

    def save_data(self, collection: str, data, **kwargs):
        """
        Save data to the collection.
        Args -
            collection (str): Name of collection.
            data : JSON / BSON document to save to the collection.
        """
        try:
            if '_id' in data:
                result = self._db[collection]. \
                    replace_one({'_id': data['_id']}, data, upsert=True)
                return {"status": STATUSES.SUCCESS.value,
                        "matched_count": result.matched_count,
                        "insert_id": None}
            else:
                result = self._db[collection].insert_one(data)
                return {"status": STATUSES.SUCCESS.value,
                        "matched_count": None,
                        "insert_id": result.inserted_id}

        except Exception as e:
            # Log.error(f"Unable to fetch data from data store. Error {e}")
            raise DBError(f"Unable to save data to data store. Error {e}")
