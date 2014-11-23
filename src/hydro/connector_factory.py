__author__ = 'moshebasanchig'

from importlib import import_module
from base_classes import Base
from connectors.base_classes import ConnectorBase
from hydro.exceptions import HydroException
DSN = 'dsn'


class ConnectionPool(Base):
    CONN_POOL_SIZE = 1
    pool = []
    logical_names = set([])

    def __init__(self, id):
        self._id = id

    def get_connection(self, data_source, conn_conf, logger):
        #TODO support pooling
        if len(self.pool) < self.CONN_POOL_SIZE:
            #get connection class
            cls = self.get_connector_class(conn_conf)
            conn = cls(conn_conf)
            conn.set_logger(logger)
            conn._connect()
            self.pool.append(conn)

        if data_source not in self.logical_names:
            self.logical_names.add(data_source)

        return self.pool[0]

    def get_connector_class(self, conn_conf):
        """
        dynamically get connector class and instantiate
        """
        # TODO: allow loading more connectors provided by the user and not just the built in ones
        path = "hydro.connectors.%s" % conn_conf.get('source_type')
        module = import_module(path)
        classes = [getattr(module, x) for x in dir(module) if isinstance(getattr(module, x), type)]
        connector_classes = filter(lambda x: issubclass(x, ConnectorBase) and x.__name__ not in
                                  ('ConnectorBase', 'DBBaseConnector'), classes)
        if len(classes) < 1 or len(connector_classes) < 1:
            raise HydroException("Connector class doesn't exist")
        con_cls = connector_classes[0]
        return con_cls


class ConnectorHandler(Base):

    pools = {}
    _logger = None

    @classmethod
    def get_connection_id(cls, conn_conf):
        """
        hashing a connection in order to check exist in connection pool
        """
        attr = ('source_type', 'connection_string', 'db_name', 'db_user', 'db_password') \
            if not conn_conf.get('dsn') \
            else 'dsn'
        conn_id = hash(''.join([conn_conf.get(att, '') for att in attr]))

        return conn_id

    def get_connection(self, data_source, conn_conf):
        """
        checking if connection pool exist if not creating and returning a connection
        """
        conn_id = self.get_connection_id(conn_conf)
        if conn_id not in self.pools:
            self.pools[conn_id] = ConnectionPool(conn_id)

        conn = self.pools[conn_id].get_connection(data_source, conn_conf, ConnectorHandler.get_logger())
        return conn

    @classmethod
    def set_logger(cls, logger):
        cls._logger = logger

    @classmethod
    def get_logger(cls):
        return cls._logger


