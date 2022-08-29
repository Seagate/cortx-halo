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


class DB(ABC):

    def __init__(self, db_endpoint, db_name) -> None:
        self._endpoint = db_endpoint
        self._db_name = db_name

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

    @abstractmethod
    def delete_data(self, data_store_name, data, **kwargs):
        pass


class STATUSES(Enum):
    SUCCESS = "success"


class MongoDB(DB):

    def __init__(self, db_endpoint: str, db_name: str) -> None:
        """Initialize Data store connection.

        Args:
            db_endpoint (str): MongoDB server endpoints.
                Ex. mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017
            db_name (str): Name of data base.
        """
        super().__init__(db_endpoint, db_name)
        # TODO : Use singleton design pattern Or make sure every
        # open connection should be closed after use.
        self.open()

    def open(self):
        """Open data store connection.

        Raises:
            DBError: Unable to open connection.
        """
        try:
            self._client = pymongo.MongoClient(self._endpoint)
            self._db = self._client[self._db_name]
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

        Keyword Args:
            **kwargs: Arbitrary keyword arguments.
            queryparams (dict): dict following pymongo convention.
            sort_query (List of tuples): (field_to_sort, sort_direction)
                direction can be ASC/ASCENDING or DSC/DESCENDING.
            limit (int): Limit for no. of documents returned by query.
            skip (int): To skip the first x records of the returned results.
            count(bool): True / False. To get the total count of documents
                irrespective of limit & skip field.

        Raises:
            DBError: Unable to fetch data.

        Returns:
            tuple: (List of records, Total count of documents)
        """
        result_list = []
        total_count = None
        query_filter = kwargs.get('queryparams')
        sort_query = kwargs.get('sort_query')
        limit = kwargs.get('limit') if kwargs.get('limit') else 0
        skip = kwargs.get('skip') if kwargs.get('skip') else 0
        count = kwargs.get('count')

        try:
            if sort_query is not None:
                sort_fields = []
                for sort_field, sort_dir in sort_query:
                    if sort_dir.upper() in ('ASC', 'ASCENDING'):
                        sort_fields.append((sort_field, pymongo.ASCENDING))
                    elif sort_dir.upper() in ('DSC', 'DESCENDING'):
                        sort_fields.append((sort_field, pymongo.DESCENDING))
                    else:
                        raise ValueError("Invalid direction for sort.\
                            Use 'ASC'/'ASCENDING' or 'DSC'/'DESCENDING'.")
            else:
                sort_fields = None

            # As per pymongo convention pass empty dict as filter
            # if query_filter is None.
            if query_filter is None:
                query_filter = {}

            results = self._db[data_store_name].find(
                filter=query_filter,
                sort=sort_fields,
                skip=skip, limit=limit)

            if count:
                total_count = self._db[data_store_name].count_documents(
                    query_filter)

            for result in results:
                result_list.append(result)
        except Exception as e:
            # Log.error(f"Unable to fetch data from data store. Error {e}")
            raise DBError(f"Unable to fetch data from data store. Error {e}")

        return result_list, total_count

    def save_data(self, data_store_name: str, data, **kwargs):
        """Save data to the data store.

        Args:
            data_store_name (str): Name of data store.
            data (json/bson): JSON / BSON document to save to the data store.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            DBError: Unable to save data.

        Returns:
            JSON: {status: "", matched_count: "", insert_id: ""}
        """
        try:
            if '_id' in data:
                result = self._db[data_store_name]. \
                    replace_one({'_id': data['_id']}, data, upsert=True)
                return {"status": STATUSES.SUCCESS.value,
                        "matched_count": result.matched_count,
                        "insert_id": None}
            else:
                result = self._db[data_store_name].insert_one(data)
                return {"status": STATUSES.SUCCESS.value,
                        "matched_count": None,
                        "insert_id": result.inserted_id}

        except Exception as e:
            # Log.error(f"Unable to fetch data from data store. Error {e}")
            raise DBError(f"Unable to save data to data store. Error {e}")

    def delete_data(self, data_store_name: str, data, **kwargs):
        """Delete data from the data store.

        Args:
            data_store_name (str): Name of data store.
            data (json/bson): JSON / BSON string.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            DBError: Failed to delete data.

        Returns:
            deleted count: 1 (Success) or 0 (Failure)
        """
        try:
            result = self._db[data_store_name].delete_one(data)
            return result.deleted_count
        except Exception as e:
            # Log.error(f"Failed to Delete data from data store. Error {e}")
            raise DBError(f"Failed to Delete data from data store. Error {e}")

    def close(self):
        """End all server sessions created by current client \
            and disconnect from MongoDB."""
        self._client.close()

    def __del__(self):
        """Close MongoDB connection."""
        self.close()
