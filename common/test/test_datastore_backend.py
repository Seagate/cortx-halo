import pytest
from datetime import datetime
from common.db_store.db import MongoDB
from common.db_store.admin_db import MongoDBAdmin

admin_db = None
db = None


@pytest.fixture
def setup_admin_db():
    global admin_db
    admin_db = MongoDBAdmin(
        endpoint="mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017",
        db_name="test")
    yield
    admin_db.close_connection()


@pytest.fixture
def setup_db():
    global db
    db = MongoDB(
        endpoint="mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017",
        db_name="test")
    yield
    db.close_connection()


def test_create_time_series_data_store(setup_admin_db):
    """Test by creating collection & listing it back."""
    admin_db.create_data_store(
        data_store="timeseries",
        data_store_name="test_coll",
        timeField="timestamp"
        )
    collection_list = admin_db.get_data_stores()
    assert 'test_coll' in collection_list, \
        "Failed to create timeseries collection."


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
