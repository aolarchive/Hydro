from hydro.topology_base import Topology
from hydro.exceptions import HydroException
from copy import deepcopy

__author__ = 'moshebasanchig'


class ResultSet(object):
    def __init__(self, plan, stream):
        self.stream = stream
        self.plan = plan


class HydroBase(object):
    """
    this class will be used
    """

    def __init__(self):
        self._topologies = dict()

    def return_topology_callback_if_exist(self, topology):
        if topology in self._topologies:
            return self._topologies[topology].submit
        return None

    def register(self, name, obj):
        if not isinstance(obj, Topology):
            raise HydroException("Not a Topology instance")
        self._topologies[name] = obj

    def submit(self, name, params=None):
        #Todo get topology from cache
        topology = self._topologies.get(name, None)
        if not topology:
            raise HydroException("Topology doesn't exist")

        #setting 2 call back functions
        #set_topology_lookup_callback to let the query engine to lookup topologies in order to use them as a stream
        topology.query_engine.set_topology_lookup_callback(self.return_topology_callback_if_exist)
        #set topology cache ttl for not being bigger than the minimum of the query engine streams
        topology.query_engine.set_topology_cache_ttl_callback(topology.topology_cache_ttl_callback)

        data = topology.submit(deepcopy(params))
        execution_plan = topology.get_execution_plan()
        return ResultSet(execution_plan, data)


class LocalHydro(HydroBase):
    """
    creating a hook for local mocking
    """
    pass
