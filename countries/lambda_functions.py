"""
Constants File

__author__: Makarand Sawarkar
__License__: Acuity KP - Alexandria
"""



from pymongo import MongoClient, errors


class DBConnect:
    """
    A class for connecting to a MongoDB instance
    """

    def __init__(self):
        """
        Initializer method for database connection
        """
        self.client = self._connect()

    def _connect(self):
        """
        Private method for establishing a connection to MongoDB
        """
        return MongoClient('localhost', 27017)

    def close_connection(self):
        """
        Public method for closing the database connection
        """
        self.client.close()


def lambda_handler(event, context):
    """
    Lambda function to retrieve all documents from a MongoDB collection
    """
    try:
        client = DBConnect().client
        db = client['alexandria_general']
        country_master = db['country_master']
        response = country_master.find({}, {'_id': 0})
        ret = list(response)
        client.close()
        if not ret:
            ret.append({'name': 'Unknown', 'population': 0})
        return {
            'isError': False,
            'body': ret
        }
    except (errors.ConnectionFailure, ValueError) as ex:
        return {
            'isError': True,
            'body': f'Error occurred: {str(ex)}'
        }
