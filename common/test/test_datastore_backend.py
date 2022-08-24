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

import pytest
from datetime import datetime
from common.db_store.db_manager import DBManager


pytestmark = pytest.mark.unit
admin_db = None
db = None


@pytest.fixture
def setup_admin_db():
    global admin_db
    admin_db = DBManager.get_admin_db_instance(
       admin_db_type='mongodb_admin',
       db_endpoint="mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017",
       db_name="test")


@pytest.fixture
def setup_db():
    global db
    db = DBManager.get_db_instance(
       db_type='mongodb',
       db_endpoint="mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017",
       db_name="test")


def test_create_time_series_data_store(setup_admin_db):
    """Test by creating data store & listing it back."""
    admin_db.create_data_store(
        data_store_type="timeseries",
        data_store_name="test_coll",
        timeField="timestamp"
        )
    collection_list = admin_db.get_data_stores()
    assert 'test_coll' in collection_list, \
        "Failed to create timeseries data store."


def test_create_index(setup_admin_db):
    """Test by creating index & listing it back."""
    admin_db.create_index("test_coll", "timestamp")
    index_list = admin_db.list_indexes("test_coll")
    assert 'timestamp_1' in index_list, "Failed to create index."


def test_save_data(setup_db):
    """Test by saving data and reading it back."""
    record = {"timestamp": datetime.now(),
              "comp": "disk", "measures": {'cpu': '23', 'memory': '235'}}
    result = db.save_data("test_coll", data=record)
    assert result is not None, "Failed to save Data."
    get_list_of_records = db.get_data("test_coll")
    assert any(r['measures'] == record['measures']
               for r in get_list_of_records)


def test_get_data(setup_db):
    """Test by listing data."""
    get_list_of_records = db.get_data("test_coll")
    assert get_list_of_records is not None, "Failed to fetch Data."


def test_delete_index(setup_admin_db):
    """Test by deleting index and confirm by listing indexes."""
    admin_db.drop_index("test_coll", "timestamp_1")
    index_list = admin_db.list_indexes("test_coll")
    assert 'timestamp_1' not in index_list, "Failed to delete index."


def test_delete_collection(setup_admin_db):
    """Test by deleting collection and confirm by listing collection."""
    admin_db.delete_data_store("test_coll")
    collection_list = admin_db.get_data_stores()
    assert 'test_coll' not in collection_list, "Failed to delete collection."
