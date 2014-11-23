__author__ = 'moshebasanchig'
from hydro import Configurator
from hydro.base_classes import HydroStr, HydroDatetime, HydroList
conf = Configurator.config_builder()
conf.OPTIMIZER = 'TopologyInjectionOptimizer'

