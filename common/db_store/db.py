from enum import Enum
import pymongo
from abc import ABC, abstractmethod
from common.db_store.error import DBError


class DB(ABC):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_data(self, data_store_name, **kwargs):
        pass

    @abstractmethod
    def save_data(self, data_store_name, data, **kwargs):
        pass


class STATUSES(Enum):
    SUCCESS = "success"


class MongoDB(DB):

    def __init__(self, endpoint: str, data_store_group: str) -> None:
        """Initialize Data store connection.

        Args:
            endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            data_store_group (str): Name of data store group.
        """
        self._endpoint = endpoint
        self._data_store_group = data_store_group
        self.open()

    def open(self):
        """Open data store connection.

        Raises:
            DBError: Unable to open connection.
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

    def get_data(self, data_store_name: str, **kwargs):
        """Get list of documents that match the query criteria.

        Args:
            data_store_name (str): Name of data store.

        Raises:
            DBError: Unable to fetch data.

        Returns:
            list: List of records.
        """
        result_list = []
        query_params = kwargs.get('queryparams')

        try:
            results = self._data_group[data_store_name].find(query_params)
            for result in results:
                result_list.append(result)
        except Exception as e:
            # Log.error(f"Unable to fetch data from data store. Error {e}")
            raise DBError(f"Unable to fetch data from data store. Error {e}")

        return result_list

    def save_data(self, data_store_name: str, data, **kwargs):
        """Save data to the data store.

        Args:
            data_store_name (str): Name of data store.
            data (json/bson): JSON / BSON document to save to the data store.

        Raises:
            DBError: Unable to save data.

        Returns:
            JSON: {status: "", matched_count: "", insert_id: ""}
        """
        try:
            if '_id' in data:
                result = self._data_group[data_store_name]. \
                    replace_one({'_id': data['_id']}, data, upsert=True)
                return {"status": STATUSES.SUCCESS.value,
                        "matched_count": result.matched_count,
                        "insert_id": None}
            else:
                result = self._data_group[data_store_name].insert_one(data)
                return {"status": STATUSES.SUCCESS.value,
                        "matched_count": None,
                        "insert_id": result.inserted_id}

        except Exception as e:
            # Log.error(f"Unable to fetch data from data store. Error {e}")
            raise DBError(f"Unable to save data to data store. Error {e}")

    def close(self):
        """End all server sessions created by current client \
            and disconnect from MongoDB."""
        self._client.close()
