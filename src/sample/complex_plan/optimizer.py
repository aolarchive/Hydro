from hydro.base_classes import PlanObject
from hydro.base_classes import OptimizerBase
from hydro.exception import HydroException


class SampleOptimizer(OptimizerBase):
    def get_plan(self, data_type, params, conf=None):
        plans = {
            'complex_data': {'plan': self._get_complex_data}
        }
        return plans[data_type]['plan'](data_type, params, conf)

    def _get_complex_data(self, data_type, params, conf):
        plan = PlanObject(params, data_type, conf)
        # TODO: configure the data source type, etc.

        if params['APP_TYPE'].to_string() == 'Dashboard':
            pass
        else:
            pass