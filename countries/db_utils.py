"""
Constants File

__author__: Deepak Kumar
__License__: Acuity KP - Alexandria
"""
import boto3
import base64
from botocore.exceptions import ClientError
SECRET = None


class ConstantValue:
    """Constant Value Class"""

    def __init__(self):
        """
        Initializer method
        """
        self.__db_engine = 'mongodb'
        self.__db_host = 'localhost'
        self.__db_port = '27017'
        self.__user = 'admin'
        self.__pwd = 'Aa147258369+'
        # self._get_db_detils(self.__get_secret())

    def __repr__(self):
        """ Db uri build getter method"""
        cred = self.__user + ':' + self.__pwd
        db_domain = '@' + self.__db_host + ':' + str(self.__db_port)
        return self.__db_engine + '://' + cred + db_domain

    def _get_db_detils(self, details):
        print("===>;", details)
        if isinstance(details, str):
            details = eval(details)
        self.__user = details.get('username')
        self.__pwd = details.get('password')
        self.__db_port = details.get('port')
        self.__db_host = details.get('host')
        # self.__db_engine = details.get('engine')

    @staticmethod
    def __get_secret():
        """Get secret keys from secret manager"""

        global SECRET
        if SECRET is None:
            secret_name = "nprd/alexandria/docdb"
            region_name = "eu-west-1"
            session = boto3.session.Session()
            client = session.client(service_name='secretsmanager', region_name=region_name)
            try:
                get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            except ClientError as err:
                print(f'Error: {err}')
            else:
                if 'SecretString' in get_secret_value_response:
                    SECRET = get_secret_value_response['SecretString']
                else:
                    SECRET = base64.b64decode(get_secret_value_response['SecretBinary'])
                return SECRET
        else:
            return SECRET


class Collections:
    us_notes = "US_FinancialStatements_Notes"
    us_cf = "US_FinancialStatements_CF"
    us_bs = "US_FinancialStatements_BS"
    us_is = "US_FinancialStatements_IS"
    us_xbrl = "US_FinancialStatements_XBRL"
    us_cf_hist = "US_FinancialStatements_CF_History"
    us_bs_hist = "US_FinancialStatements_BS_History"
    us_is_hist = "US_FinancialStatements_IS_History"
    us_notes_hist = "US_FinancialStatements_Notes_History"
    us_10k_text = "US_10KFilingText"
    us_submission = "US_SEC_Submission"
    us_patent = "US_Patents"
    us_db = "alexandria_US"
    us_filing_live = "alexandria_Live"
    us_live_db = "US_Current_Filings"


CA_CERTIFICATE_FILE = 'ca-bundle.pem'

ConstantValue()
