from __future__ import absolute_import

from hydro.connectors.base_classes import DBBaseConnector
from hydro.exceptions import HydroException

connector_type = None
try:  # TODO: MySQLdb offers greater performance in exchange for requiring the libs to be installed. It should be the default
    from mysql.connector import connect as mysql_connect
    connector_type = 'mysql.connector'
except ImportError:
    from MySQLdb import connect as mysql_connect
    connector_type = 'MySQLdb'

__author__ = 'moshebasanchig'

DSN = 'dsn'


class MySqlConnector(DBBaseConnector):
    """
    implementation of mysql connector, base function that need to be implemented are _connect, _close and _execute
    """
    def _connect(self):
        if self._conf_defs['connection_type'] == DSN:
            raise HydroException("Mysql dsn connection is not implemented")
        else:
            if connector_type == 'MySQLdb':
                db_var = 'db'
                password_var = 'passwd'
            elif connector_type == 'mysql.connector':
                db_var = 'database'
                password_var = 'password'

            #TODO need to be implemented based on connection string
            # conn_string = 'DSN=%s' % self._conf_defs['connection_string']
            # self.logger.debug('Connect to {0}'.format(conn_string))
            db_params = {'user': self._conf_defs['db_user'],
                         password_var: self._conf_defs['db_password'],
                         'host': self._conf_defs['connection_string']}
            if self._conf_defs['db_name']:
                db_params[db_var] = self._conf_defs['db_name']
            self._conn = mysql_connect(**db_params)

if __name__ == '__main__':
    params = {
        'source_type': 'mysql',
        'connection_type': 'connection_string',
        'connection_string': '127.0.0.1',
        'db_name': 'test',
        'db_user': 'root',
        'db_password': 'xxx'
    }
    con = MySqlConnector(params)
    print con.execute('select 1 a')
