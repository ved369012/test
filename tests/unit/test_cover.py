import csv
import pytest
import sys

sys.path.insert(0,'../../countries')
from lambda_functions import lambda_handler

from unittest.mock import Mock, patch
from pymongo.collection import Collection


def get_test_data(filename = 'Countries_data.csv'):
    # reading the csv file
    with open(filename, 'r') as filePointer:
        fileData = csv.DictReader(filePointer, skipinitialspace=True, delimiter=',')
        test_data = [{k: v for k, v in row.items()} for row in fileData]
        return test_data


@pytest.fixture(scope='function')
def mocked_db_collection():
    """
    Fixture to create and return a mocked Collection object
    """
    mocked_collection = Mock(spec=Collection)
    # mocked_collection.find.return_value = [{'name': 'USA', 'population': 328200000},
    #                                        {'name': 'Canada', 'population': 37600000}]
    mocked_collection.find.return_value = get_test_data()
    return mocked_collection


@pytest.fixture(scope='function')
def mocked_db_connection(monkeypatch, mocked_db_collection):
    """
    Fixture to create and return a mocked MongoDB connection
    """
    mocked_connection = {'alexandria_General': {'Country_Master': mocked_db_collection}}
    monkeypatch.setattr('pymongo.MongoClient', lambda *args, **kwargs: mocked_connection)
    return mocked_connection


def test_lambda_handler_empty_collection(mocked_db_connection):
    """
    Test lambda_handler function when the collection is empty
    """
    mocked_db_collection = mocked_db_connection['alexandria_General']['Country_Master']
    mocked_db_collection.find.return_value = []
    expected_response = {
        'isError': False,
        'body': [{'name': 'Unknown', 'population': 0}]
    }
    result = lambda_handler(None, None)
    if result != expected_response:
        raise AssertionError(f"Expected {expected_response}, but got {result}")

