__author__ = 'yanivshalev'

import unittest
from hydro.connectors.vertica import VerticaConnector



class VerticaConnectorTest(unittest.TestCase):

    def test_fail_dsn(self):
        self.assertRaises(Exception, VerticaConnector({'source_type': 'vertica',
                                                       'connection_type': 'dsn', 'connection_string': '',
                                                       'db_name': '', 'db_user': '','db_password': ''})._verify_connection_definitions)

    def test_fail_user(self):
        self.assertRaises(Exception, VerticaConnector({'source_type': 'vertica',
                                                       'connection_type': 'conn_sting', 'connection_string': 'x@x.com',
                                                       'db_name': '', 'db_user': '','db_password': 'pass'})._verify_connection_definitions)

    def test_fail_password(self):
        self.assertRaises(Exception, VerticaConnector({'source_type': 'vertica',
                                                       'connection_type': 'conn_sting', 'connection_string': 'x@x.com',
                                                       'db_name': '', 'db_user': 'user', 'db_password': ''})._verify_connection_definitions)

    def test_fail_connection_string(self):
        self.assertRaises(Exception, VerticaConnector({'source_type': 'vertica',
                                                       'connection_type': 'conn_sting', 'connection_string': '',
                                                       'db_name': '', 'db_user': 'user','db_password': 'pass'})._verify_connection_definitions)





if __name__ == '__main__':
    unittest.main()