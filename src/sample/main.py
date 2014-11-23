__author__ = 'moshebasanchig'

from hydro.hydro_cluster import LocalHydro
from hydro.exceptions import HydroException
from geo_queries.geo_widget_topology import GeoWidgetTopology
from topology_injection.topology_injection_topology import TopologyInjectionTopology
from hydro.common.configurator import Configurator
from hydro.common.logger import Logger
import logging

if __name__ == '__main__':
    data = None
    params = {
        'FROM_DATE': '2014-07-01',
        'TO_DATE': '2014-07-31',
        'CLIENT_ID': 'a-client',
        'EVENT_TYPES': ['pay', 'sell'],
        'APP_TYPE': 'Dashboard'
    }
    local_hydro = LocalHydro()
    Configurator.DATABASES['dashboard_db'] = {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'dashboard_db',
        'OPTIONS': {'compress': True,
                    'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;'},
        'PASSWORD': 'xxxx',
        'USER': 'root'
    }
    Configurator.DATABASES['cache'] = Configurator.DATABASES['dashboard_db']
    # HACK: this is one hell of a hack. Without a DATABASE_ROUTERS configuration, django will opt to take 'default'
    Configurator.DATABASES['default'] = Configurator.DATABASES['dashboard_db']
    Logger.set_logger(logging.getLogger("HydroSample"))
    geo_logger = logging.getLogger("GeoLogger")
    # in case we'd want to use mysql cache, the following configuration is required
    cache_config = {
        'cache_engine_name': Configurator.CACHE_ENGINE_MYSQL_CACHE,
        'params': {
            'cache_db': 'dashboard_db',
            'cache_table': 'hydro_cache'
        }
    }
    local_hydro.register('GeoWidget', GeoWidgetTopology(cache_engine=cache_config, logger=geo_logger))
    local_hydro.register('TopologyInjector', TopologyInjectionTopology(cache_engine=Configurator.CACHE_ENGINE_IN_MEMORY))

    try:
        #result = local_hydro.submit('TopologyInjector', params)
        result = local_hydro.submit('GeoWidget', params)

        local_hydro.submit('GeoWidget', params)  # the cache should be used here
    except HydroException, e:
        print "Encountered an exception:", e.message
    result = local_hydro.submit('GeoWidget', params)
