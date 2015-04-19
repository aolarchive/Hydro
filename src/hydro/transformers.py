__author__ = 'moshebasanchig'

from base_classes import Base
import pandas as pd


class Transformers(Base):
    def __init__(self):
        self._execution_plan = None

    def combine(self, stream1, stream2, left_on=None, right_on=None, how='inner'):
        """
        takes two input streams (pandas data frames) and joins them based on the keys dictionary
        """
        if self._execution_plan:
            self._execution_plan.append('combine', 'transform')

        if left_on and right_on:
            return pd.merge(stream1, stream2, left_on=left_on, right_on=right_on, how=how)
        else:
            return None

    def aggregate(self, stream, group_by=None, operators=None):
        """
        takes an input stream (pandas data frame) and perform a group-by + aggregation.
        for instance: aggregate(data, group_by=['col1'], operators={'col2': 'sum'})
        """
        if self._execution_plan:
            self._execution_plan.append('aggregate', 'transform')

        if group_by and operators:
            return stream.groupby(group_by).agg(operators)
        else:
            return None