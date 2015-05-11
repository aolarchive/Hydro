__author__ = 'moshebasanchig'

from hydro.common.logger import get_logger
from hydro.stats_engine import stats_engine
from hydro import Configurator
from hydro.types import *
from django.template import Template, Context

ALL = 'ALL'


class Base(object):
    """
    Hydro base class supplies the following tool set
    1. logger
    2. stats engine

    """
    def __init__(self):
        self.logger = get_logger()
        self.stats = stats_engine


class HydroCommandTemplate(object):
    """
    Command will generate a stream command, it can be SQL, Shell commands, Hbase scans and etc
    parse returns a rendered command after injecting the parameters into their placements
    """
    def __init__(self, templates_dir, template_file):
        # TODO: the following line assumes Unix separators
        with open('%s/%s' % (templates_dir, template_file), 'r') as f:
            template = f.read()
        self._template = Template(template)

    @property
    def template(self):
        return self._template

    def parse(self, params):
        context = Context()
        for key, value in params.iteritems():
            if value:
                context[key] = value.to_string()

        return self._template.render(context)


class PlanObject(Base):
    """
    creating a logical plan from data source and template file
    PLEASE NOTE: params dictionary is changed with parsed parameter objects
    """
    def __init__(self, params, source_id=None, config=None, segment_id=ALL):
        super(PlanObject, self).__init__()
        self._data_source = None
        self._template_file = None
        self._source_type = None
        plan_allowed_parameters = getattr(config, 'PLAN_ALLOWED_PARAMETERS', {})
        if not set(params.keys()).issubset(set(plan_allowed_parameters.keys())):
            raise HydroException("Some parameters are not registered as valid in PLAN_ALLOWED_PARAMETERS")
        for key in params:
            tp = plan_allowed_parameters[key]['type']
            try:
                val = params[key]
                is_optional = plan_allowed_parameters[key].get('optional', False)
                if is_optional and val is None:
                    obj = val
                elif not isinstance(val, HydroType):
                    obj = tp(val, **plan_allowed_parameters[key])
                else:
                    obj = val
                self.__dict__[key] = obj
                params[key] = obj
            except:
                raise HydroException('Parsing parameter {0} failed with value {1}'.format(key, val.value))
        self.logger = get_logger()
        self._sampling = False
        self.gather_statistics(source_id, segment_id)

    def gather_statistics(self, source_id, segment_id):
        stats = self.stats.gather_statistics(source_id, segment_id)

        for key in Configurator.OPTIMIZER_STATISTICS[ALL]:
            #getting the default statistics
            default = Configurator.OPTIMIZER_STATISTICS[ALL][key]
            #getting specific statistics, first by segment id if not exist then by source id
            per_source = Configurator.OPTIMIZER_STATISTICS.get(source_id, {})
            per_segment = per_source.get(segment_id, {})
            val = per_segment.get(key) if per_segment.get(key) else per_source.get(key)
            configuration_val = val if val else default

            #injecting stats to plan object
            if Configurator.USE_STATS_DB:
                self.__dict__[key] = stats.get(key).max() if stats.get(key).__len__() else configuration_val
            else:
                self.__dict__[key] = configuration_val

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, value):
        self._data_source = value

    @property
    def template_file(self):
        return self._template_file

    @template_file.setter
    def template_file(self, value):
        self._template_file = value

    @property
    def source_type(self):
        return self._source_type

    @source_type.setter
    def source_type(self, value):
        self._source_type = value

    @property
    def sampling(self):
        return self._sampling

    @sampling.setter
    def sampling(self, value):
        self._sampling = value


class OptimizerBase(Base):
    def __init__(self):
        self.logger = get_logger()
        self.stats = stats_engine

    def get_plan(self, source_id, params):
        self.logger('Using default plan')
        plan = PlanObject(params, source_id, Configurator.config_builder())
        # here comes the logic around the params
        return plan


if __name__ == '__main__':
    #print ConnectorBase().execute('select 1')
    print HydroStr(1).to_string()