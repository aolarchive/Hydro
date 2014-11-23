__author__ = 'moshebasanchig'

import pandas as pd
from hydro.exceptions import HydroException

DSN = 'dsn'


class ConnectorBase(object):

    _conn = None

    def __init__(self):
        self.logger = None

    def _verify_connection_definitions(self):
        raise HydroException("Not implemented")

    def _connect(self):
        raise HydroException("Not implemented")

    def _close(self):
        raise HydroException('Not implemented')

    def execute(self):
        raise HydroException('Not implemented')

    def close(self):
        self.logger.debug('Closing connection')
        self._close()
        self._conn = None
        return True

    def connect(self):
        if not self._conn:
            self.logger.debug('Connection does not exist, Verify definitions of connection')
            self._verify_connection_definitions()
            self._connect()
        return True

    def execute(self, command):
        self.connect()

        try:
            self.logger.debug('Executing command: {0}'.format(command))
            res = self._execute(command)
            return res

        except Exception, err:
            self.logger.error('Error: {0}'.format(err.message))
            self.close()
            raise err

    def set_logger(self, logger):
        self.logger = logger


class DBBaseConnector(ConnectorBase):
    """
    implementation of DB base connector, base function that need to be implemented are _connect, _close and _execute
    """
    def __init__(self, conn_definitions):
        self._conn = None
        self._conf_defs = conn_definitions
        super(DBBaseConnector, self).__init__()

    def _convert_results_to_dataframe(self, cursor):
        """
        This is deprecated - use SQLAlchemy and pandas' read_sql method instead
        """
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        if isinstance(rows, tuple):
            rows = list(rows)
        data = pd.DataFrame.from_records(rows, columns=columns)
        return data

    def _verify_connection_definitions(self):
        """
        Verifies if connection configuration is complete
        """
        if self._conf_defs['connection_type'] == DSN:
            if not self._conf_defs['connection_string']:
                raise HydroException('Connection dsn is Null')
        else:
            for att in ('db_user', 'db_password', 'connection_string'):
                if not self._conf_defs.get(att):
                    raise HydroException('Connection {0} is Null'.format(att))

    def _execute(self, command):
        """
        base class
        """
        cursor = self._conn.cursor()
        cursor.execute(command)
        result = self._convert_results_to_dataframe(cursor)
        cursor.close()
        return result

    def _close(self):
        self._conn.close()
