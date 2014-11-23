__author__ = 'moshebasanchig'
from hydro import Configurator
from hydro.base_classes import HydroStr, HydroDatetime, HydroList
conf = Configurator.config_builder()
conf.OPTIMIZER = 'GeoQueriesOptimizer'

# TODO: this will have to come from the application level, e.g in hydro.initialize(conf_obj)
conf.CONNECTIONS = {
    'vertica-dashboard': {
        'source_type': 'vertica',
        'connection_type': 'dsn',
        'connection_string': 'VerticaDSN',
        'db_name': '',
        'db_user': '',
        'db_password': ''
    }
}

conf.PLAN_ALLOWED_PARAMETERS = {'CLIENT_ID': {'type': HydroStr},
                               'FROM_DATE': {'type': HydroDatetime},
                               'TO_DATE': {'type': HydroDatetime},
                               'EVENT_TYPES': {'type': HydroList, 'optional': True},
                               'APP_TYPE':{'type': HydroStr},
                               }