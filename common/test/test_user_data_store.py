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

import uuid
import pytest
from common.data_stores.data_store import UserMgmtStore
from common.db_store.db_manager import DBManager


pytestmark = pytest.mark.unit
data_store = None
admin_db = None


@pytest.fixture
def setup_datastore():
    global data_store
    data_store = UserMgmtStore(
        'mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017',
        db_name='test', data_store_name='user_mgmt')


@pytest.fixture
def setup_admin_db():
    global admin_db
    admin_db = DBManager.get_admin_db_instance(
       admin_db_type='mongodb_admin',
       db_endpoint="mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017",
       db_name="test")


def test_save_data(setup_datastore):
    """Test by saving data and reading it back."""
    record = {
        "user_id": str(uuid.uuid4().hex),
        "username": "admin",
        "password": "admin",
        "email": "admin@gmail.com",
        "user_type": "manager"
    }
    result = data_store.store_data(data=record)
    assert result is not None, "Failed to save Data."

    get_list_of_records = data_store.get_data()
    assert any(r['username'] == record['username']
               for r in get_list_of_records)


def test_get_data(setup_datastore):
    """Test by listing data."""
    get_list_of_records = data_store.get_data()
    assert get_list_of_records is not None, "Failed to fetch Data."


def test_delete_data(setup_datastore):
    """Test by deleting data."""
    record = {
        "username": "admin"
    }
    result = data_store.delete_data(data=record)
    assert result, "Failed to Delete Data."


# Clean Up.
def test_delete_collection(setup_admin_db):
    """Delete collection."""
    admin_db.delete_data_store("user_mgmt")
