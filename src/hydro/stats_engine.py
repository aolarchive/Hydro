__author__ = 'yanivshalev'
from hydro.common.configurator import Configurator


class StatsEngine(object):
    _stats = {}

    def __init__(self):
        if Configurator.USE_STATS_DB:
            # TODO: support stats engines which doesn't rely on mysql
            from connectors.mysql import MySqlConnector

            params = {
                'connection_type': 'connection_string',
                'connection_string': Configurator.DATABASES['stats']['HOST'],
                'db_name': Configurator.DATABASES['stats']['NAME'],
                'db_user': Configurator.DATABASES['stats']['USER'],
                'db_password': Configurator.DATABASES['stats']['PASSWORD']
            }

            self._conn = MySqlConnector(params)
            self.gather_statistics = self._gather_statistics
        else:
            self.gather_statistics = lambda x, y: None

    def _gather_statistics(self, source_id, segment_id):

        keys = Configurator.OPTIMIZER_STATISTICS['ALL'].keys()
        res = self._conn.execute("SELECT {0} FROM {1} WHERE source_id = '{2}' and segment_id = '{3}' "
                                 .format(','.join(keys), 'source_statistics', source_id, segment_id))
        return res

stats_engine = StatsEngine()
