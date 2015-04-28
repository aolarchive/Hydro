from hydro.topology_base import Topology


class SampleTopology(Topology):  # TODO: rename this class and the entire file
    def _submit(self, params):
        """
        topology consists of several steps, defining one source stream or more, combining and transformations
        """
        main_stream = self.query_engine.get('complex_data', params)
        return main_stream