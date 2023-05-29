import unittest
import sys
sys.path.insert(0,'../../countries')
from lambda_functions import lambda_handler


class TestLambdaHandler(unittest.TestCase):
    """
    Test class for lambda_handler method
    """

    def test_lambda_handler_success(self):
        """
        Test lambda_handler success scenario
        """
        # Arrange
        event = {}
        context = {}

        # Act
        result = lambda_handler(event, context)

        # Assert
        self.assertFalse(result['isError'])
        self.assertGreater(len(result['body']), 0)
