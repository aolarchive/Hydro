__author__ = 'moshebasanchig'

from hydro.topology_base import Topology


class TopologyInjectionTopology(Topology):
    def _submit(self, params):
        """
        topology consists of several steps, defining one source stream or more, combining and transformations
        """
        main_stream = self.query_engine.get('DeviceGridWidget', params)
        return main_stream