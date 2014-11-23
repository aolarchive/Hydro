__author__ = 'yanivshalev'
from hydro import Configurator
from hydro.base_classes import HydroStr, HydroDatetime, HydroList
conf = Configurator.config_builder()
conf.OPTIMIZER = 'TestTopology'

# TODO: this will have to come from the application level, e.g in hydro.initialize(conf_obj)

conf.PLAN_ALLOWED_PARAMETERS = {'CLIENT_ID': {'type': HydroStr},
                               'FROM_DATE': {'type': HydroDatetime},
                               'TO_DATE': {'type': HydroDatetime},
                               'EVENT_TYPES': {'type': HydroList}
                            }

