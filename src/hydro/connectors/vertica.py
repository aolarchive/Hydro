__author__ = 'moshebasanchig'

from hydro.connectors.base_classes import DBBaseConnector, DSN, CONNECTION_STRING
import pyodbc
from hydro.exceptions import HydroException


class VerticaConnector(DBBaseConnector):
    """
    implementation of Vertica connector, base function that need to be implemented are _connect, _close and _execute
    """
    def _connect(self):
        if self._conf_defs['connection_type'] == DSN:
            conn_string = 'DSN=%s' % self._conf_defs['connection_string']
            self.logger.debug('Connect to {0}'.format(conn_string))
            self._conn = pyodbc.connect(conn_string, unicode_results=True)
        elif self._conf_defs['connection_type'] == CONNECTION_STRING:
            self._conn = pyodbc.connect(self._conf_defs['connection_string'], unicode_results=True)
        else:
            #TODO need to be implemented based on connection string
            raise HydroException("Vertica connection string connection is not implemented")

if __name__ == '__main__':
    params = {
        'source_type': 'vertica',
        'connection_type': 'dsn',
        'connection_string': 'VerticaDSN',
        'db_name': '',
        'db_user': '',
        'db_password': ''
    }
    con = VerticaConnector(params)
    print con.execute('select 1')