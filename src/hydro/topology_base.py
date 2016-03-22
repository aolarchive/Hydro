from hydro.common.execution_plan import ExecutionPlan
from hydro.transformers import Transformers
from hydro.query_engine_factory import QueryEngineFactory
from base_classes import Base
from hydro.common.utils import create_cache_key
from hydro.cache import CacheEnginesFactory
import inspect
from hydro.exceptions import HydroException
from hydro.common.configurator import Configurator
from hashlib import md5
import os
from django.conf import settings
import django


__author__ = 'moshebasanchig'


class Topology(Base):
    def __init__(self, cache_engine=Configurator.CACHE_ENGINE_IN_MEMORY, base_dir=None, cls=None, logger=None):
        super(Topology, self).__init__()

        # Initializing django here in case Hydro is not used within a django project
        if 'DJANGO_SETTINGS_MODULE' not in os.environ:
            if not settings.configured:
                settings.configure()
                django.setup()

        if logger:
            self.logger = logger

        # TODO: read the cache engines from the configuration and allow passing parameters if needed
        # Topology is support self discovering of its needed modules but it can be supplied in init
        if not base_dir:
            base_dir = self.__module__
        if not cls:
            cls = self.__class__

        self.cache_engines = CacheEnginesFactory.get_cache_engines()
        self.transformers = Transformers()
        self.base_dir = '.'.join(base_dir.split('.')[:-1])
        self._modules_dir = self.base_dir
        self._templates_dir = os.path.dirname(inspect.getabsfile(cls))

        cache_engine_params = None
        if type(cache_engine) == dict:
            cache_engine_name = cache_engine['cache_engine_name']
            cache_engine_params = cache_engine['params']
        else:
            cache_engine_name = cache_engine
        cache_engine_class = self.cache_engines.get(cache_engine_name)
        if not cache_engine_class:
            cache_engine_class = self.cache_engines.get(Configurator.CACHE_ENGINE_IN_MEMORY)
        self.cache_engine = cache_engine_class(cache_engine_params)

        self._execution_plan = ExecutionPlan()
        self.query_engine = QueryEngineFactory.get_query_engine(self._modules_dir, self.cache_engine, self._execution_plan, self.logger)
        self.query_engine.set_templates_dir(self._templates_dir)
        self.logger.debug("Topology {0} was instantiated, modules_dir: {1}, templates_dir: {2}".
                          format(type(self).__name__, self._modules_dir, self._templates_dir))

        self._topology_cache_ttl = Configurator.CACHE_DB_KEY_EXPIRE

    def _submit(self, params):
        raise HydroException('Not implemented')

    def set_topology_cache_ttl(self, cache_ttl):
        """
        cache_ttl values:
        0 - no cache
        >0 - seconds
        None - forever
        """
        self._topology_cache_ttl = cache_ttl

    def topology_cache_ttl_callback(self, cache_ttl):
        """
        topology ttl should be equal to the minimum of its query cache ttl
        """
        if cache_ttl < self._topology_cache_ttl:
            self.logger.debug('Topology cache ttl was set to {0} seconds, by one of its query streams'.format(cache_ttl))
            self.set_topology_cache_ttl(cache_ttl)

    def submit(self, params):
        hash_value = md5()
        hash_value.update(str(params))
        cache_key = create_cache_key('topology_cache_key+' + self.__class__.__name__ + hash_value.digest())
        data = self.cache_engine.get(cache_key)
        hit = False if data is None else True
        self._execution_plan.add_phase(self, "submit", {'topology_cache_hit': hit})
        if not hit:
            self.logger.debug('Topology cache miss, cache_key: {0}'.format(cache_key))
            data = self._submit(params)
            cache_params = {'key': cache_key, 'value': data}
            # in case there is a ttl
            cache_params['ttl'] = self._topology_cache_ttl
            self.cache_engine.put(**cache_params)

        else:
            self.logger.debug('Topology cache hit, cache_key: {0}'.format(cache_key))
        return data

    def get_execution_plan(self):
        return self._execution_plan