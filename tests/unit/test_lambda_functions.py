import csv
import unittest
import sys
sys.path.insert(0,'../../countries')
# from unittest.mock import MagicMock, patch
from lambda_functions import lambda_handler
from unittest.mock import MagicMock, patch



class TestLambdaHandler(unittest.TestCase):

    def __get_test_data(self, *args, **kwargs):
        # reading the csv file
        with open('Countries_data.csv', 'r') as filePointer:
            test_data = [{k: v for k, v in row.items()} for row in csv.DictReader(filePointer, skipinitialspace=True, delimiter=',')]
        return test_data

    def setUp(self):
        # Patching MongoClient to return a MagicMock object for testing purposes
        self.mock_client = MagicMock()
        self.mock_db = self.mock_client['test_db']
        self.mock_cm = self.mock_db['Country_Master']
        self.mock_cm.find.return_value = self.__get_test_data()
        # self.mock_cm.find.return_value = [{'name': 'USA', 'population': 330000000},
        #                                   {'name': 'India', 'population': 1380000000}]
        self.patcher = patch('lambda_functions.MongoClient', return_value=self.mock_client)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_lambda_handler_success(self):
        """
        Test if lambda_handler returns expected result when there is no error
        """
        expected_result = {
            'isError': False,
            'body': self.__get_test_data()
            # 'body':[{'name': 'USA', 'population': 330000000}, {'name': 'India', 'population': 1380000000}]
        }
        result = lambda_handler(None, None)
        self.assertEqual(result, expected_result)

    def test_lambda_handler_failure(self):
        """
        Test if lambda_handler returns expected result when there is an error
        """
        self.mock_cm.find.side_effect = Exception('Connection error')
        expected_result = {
            'isError': True,
            'body': 'Error occured: Connection error'
        }
        result = lambda_handler(None, None)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
