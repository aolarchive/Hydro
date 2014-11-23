__author__ = 'yanivshalev'

import unittest
from hydro.connectors.base_classes import ConnectorBase
from hydro.common.logger import get_logger


class ConnectorBaseTest(unittest.TestCase):

    def setUp(self):
        self.logger = get_logger()

    def test_fail_verify_connection_definitions_if_not_override(self):
        """
        fail if _connect is not implemented
        """
        connector = ConnectorBase()
        connector.logger = self.logger
        connector._connect = lambda: 1
        self.assertRaises(Exception, connector.connect)

    def test_fail_connect_if_not_override(self):
        """
        fail if _connect is not implemented
        """
        connector = ConnectorBase()
        connector.logger = self.logger
        self.assertRaises(Exception, connector.execute, 'select 1')

    def test_connect(self):
        """
        checks if connect wraps _connect and returns True
        """
        connector = ConnectorBase()
        connector.logger = self.logger
        connector._connect = lambda: 1
        connector._verify_connection_definitions = lambda: 1
        self.assertTrue(connector.connect(), True)

    def test_fail_execute_if_not_override(self):
        """
        fail _execute if not implemented
        """
        connector = ConnectorBase()
        connector.logger = self.logger
        connector._connect = lambda: 1
        connector._verify_connection_definitions = lambda: 1
        connector._conn = 'Mock'
        self.assertRaises(Exception, connector.execute, 'select 1')

    def test_execute(self):
        """
        test if execute is not failing
        """
        connector = ConnectorBase()
        connector.logger = self.logger
        connector._connect = lambda: 1
        connector._verify_connection_definitions = lambda: 1
        connector._conn = 'Mock'
        connector._execute = lambda x: 'results'
        self.assertEquals(connector.execute('select 1'), 'results')

    def test_fail_close_if_not_override(self):
        """
        fail _close if not implemented
        """

        connector = ConnectorBase()
        connector.logger = self.logger
        connector._connect = lambda: 1
        connector._verify_connection_definitions = lambda: 1
        connector._conn = 'Mock'
        connector._execute = lambda x: 'results'
        self.assertEquals(connector.execute('select 1'), 'results')
        self.assertRaises(Exception, connector.close)


    def test_close(self):
        """
        fail _close if not implemented
        """
        connector = ConnectorBase()
        connector.logger = self.logger
        connector._connect = lambda: 1
        connector._verify_connection_definitions = lambda: 1
        connector._conn = 'Mock'
        connector._execute = lambda x: 'results'
        self.assertEquals(connector.execute('select 1'), 'results')
        connector._close = lambda: 1
        self.assertEquals(connector.close(), True)

    def test_fail_close_if_not_override_internal_exception1(self):
        """
        fail _close if not implemented
        """

        connector = ConnectorBase()
        connector.logger = self.logger
        connector._connect = lambda: 1
        connector._verify_connection_definitions = lambda: 1
        connector._conn = 'Mock'
        connector._execute = lambda: 1/0
        self.assertRaises(Exception, connector.execute, 'select 1')


if __name__ == '__main__':
    unittest.main()
