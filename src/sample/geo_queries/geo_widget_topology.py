__author__ = 'moshebasanchig'

from hydro.topology_base import Topology


class GeoWidgetTopology(Topology):
    def _submit(self, params):
        """
        topology consists of several steps, defining one source stream or more, combining and transformations
        """
        main_stream = self.query_engine.get('geo_widget', params)
        lookup_stream = self.query_engine.get('geo_lookup', params, cache_ttl=1)
        combined = self.transformers.combine(main_stream, lookup_stream, left_on=['user_id'], right_on=['user_id'])
        aggregated = self.transformers.aggregate(combined, group_by=['country'], operators={'revenue': 'sum', 'spend': 'sum'})
        aggregated['ROI'] = aggregated.revenue/(aggregated.spend+aggregated.revenue)
        return aggregated