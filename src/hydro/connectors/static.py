__author__ = 'moshebasanchig'

from hydro.connectors.base_classes import ConnectorBase
from hydro.exceptions import HydroException


class StaticConnector(ConnectorBase):
    """
    implementation of a static file connector
    """
    def __init__(self, conn_definitions):
        super(ConnectorBase, self).__init__()

    def _verify_connection_definitions(self):
        pass

    def _connect(self):
        pass

    def _execute(self, command):
        return command

    def _close(self):
        pass

