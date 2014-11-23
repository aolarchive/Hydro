__author__ = 'moshebasanchig'

from importlib import import_module
from base_classes import Base, HydroCommandTemplate
from hydro.common.utils import create_cache_key
from copy import deepcopy


class QueryEngine(Base):
    def __init__(self, modules_dir, connection_handler, cache_engine, execution_plan, logger):
        # TODO: check for the existence of the dir and file and throw error otherwise
        self._modules_dir = modules_dir
        self._templates_dir = modules_dir
        self._execution_plan = execution_plan
        self._conf = import_module('%s.conf' % self._modules_dir).conf

        optimizer_class_name = self._conf.OPTIMIZER
        optimizer_class = getattr(__import__('%s.optimizer' % self._modules_dir, fromlist=[optimizer_class_name]),
                                  optimizer_class_name)
        self.optimizer = optimizer_class()
        self.connections = self._conf.CONNECTIONS
        self.con_handler = connection_handler
        self.cache = cache_engine
        self._logger = logger

    def _build_plan(self, logic_plan, params):
        template = HydroCommandTemplate(self._templates_dir, logic_plan.template_file)
        execution_plan = template.parse(params)
        return execution_plan

    @staticmethod
    def _get_cache_key(data_source_name, execution_plan):
        return create_cache_key(data_source_name + execution_plan)

    def get(self, source_id, params, cache_ttl=None):
        """
        query engine is responsible of
        1. check if params are in the allowed list
        2. getting logical plan from optimizer with flags
        3. instantiate templates with params
        4. check if exist in cache (default)

        """
        run_topology = self.return_if_topology(source_id)
        if run_topology:
            return run_topology(deepcopy(params))
        #if not topology then it's a query
        logic_plan = self.optimizer.get_plan(source_id, params, self._conf)
        plan = self._build_plan(logic_plan, params)

        # TODO: have some real logic for which plan to take. in the meanwhile, take the first
        conn_conf = self.connections.get(logic_plan.data_source)
        connection = self.con_handler.get_connection(logic_plan.data_source, conn_conf)

        cache_key = self._get_cache_key(logic_plan.data_source, plan)
        data = self.cache.get(cache_key)
        hit = False if data is None else True
        self._execution_plan.add_phase(self, logic_plan.data_source+'/'+logic_plan.template_file, {'query_cache_hit': hit})

        if not hit:
            self._logger.debug('QueryEngine cache miss, cache_key: {0}'.format(cache_key))
            data = connection.execute(plan)
            cache_params = {'key': cache_key, 'value': data}
            #in case there is a ttl
            if cache_ttl:
                cache_params['ttl'] = cache_ttl
                self.set_topology_cache_ttl(cache_ttl)

            self.cache.put(**cache_params)
        else:
            self._logger.debug('QueryEngine cache hit, cache_key: {0}'.format(cache_key))

        return data

    def get_config_item(self, key):
        if hasattr(self._conf, key):
            return getattr(self._conf, key)
        return None

    def set_templates_dir(self, templates_dir):
        self._templates_dir = templates_dir

    def set_topology_lookup_callback(self, callback_function):
        """
        call back function to lookup Hydro registered topologies
        """
        self.return_if_topology = callback_function

    def return_if_topology(self, source_id):
        """
        defining the hook for the call back function
        """
        return None

    def set_topology_cache_ttl_callback(self, callback_function):
        """
        call back function to set topology ttl
        """
        self.set_topology_cache_ttl = callback_function

    def set_topology_cache_ttl(self, cache_ttl):
        """
        defining the hook for the call back function
        """
        return None
