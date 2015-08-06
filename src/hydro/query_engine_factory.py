__author__ = 'moshebasanchig'

from hydro.query_engine import QueryEngine
from connector_factory import ConnectorHandler


class QueryEngineFactory(object):
    # cache_engines and conn_handler are singletons, hence they are static
    # moreover, conn_handler is lazy initialized
    conn_handler = None

    @classmethod
    def __get_conn_handler(cls):
        if cls.conn_handler is None:
            cls.conn_handler = ConnectorHandler()
        return cls.conn_handler

    @classmethod
    def get_query_engine(cls, engine_type, cache_engine_instance, execution_plan, logger):
        cls.__get_conn_handler().set_logger(logger)
        query_engine = QueryEngine(engine_type, cls.conn_handler, cache_engine_instance, execution_plan, logger)
        return query_engine