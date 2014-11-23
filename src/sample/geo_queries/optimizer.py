__author__ = 'moshebasanchig'

from hydro.base_classes import PlanObject
from hydro.base_classes import OptimizerBase


class GeoQueriesOptimizer(OptimizerBase):
    def get_plan(self, source_id, params, conf):
        """
        a plan is a simple tuple
        """
        plans = {
            'geo_widget': {'plan': self._geo_widget_plan,
                           },
            'geo_lookup': {'plan': self._geo_lookup_plan
                           },
        }
        return plans[source_id]['plan'](source_id, params, conf)

    def _geo_widget_plan(self, source_id,  params, conf):
        plan = PlanObject(params, source_id, conf)
        # here comes the logic around the params
        plan.data_source = 'vertica-dashboard'
        plan.template_file = 'geo_widget.sql'
        return plan

    def _geo_lookup_plan(self, source_id,  params, conf):
        plan = PlanObject(params, source_id, conf)
        plan.data_source = 'vertica-dashboard'
        plan.template_file = 'geo_lookup.sql'
        return plan