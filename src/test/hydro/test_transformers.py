__author__ = 'Yaniv Ranen'

import unittest
from hydro.transformers import Transformers
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from numpy import nan

class TransformersTest(unittest.TestCase):
    #creating data frames for the tests and results
    test_df_1 = DataFrame({'id': ['1', '2'], 'name': ['try1', 'try2']})
    test_df_2 = DataFrame({'id': ['1', '3'], 'full_name': ['full_try1', 'full_try3']})
    test_df_3 = DataFrame({'id': ['1', '2'], 'full_name': ['try1', 'try2']})

    test_result_1 = DataFrame({'id': ['1'], 'name': ['try1'], 'full_name': ['full_try1']})[["id", "name", "full_name"]]
    test_result_2 = DataFrame({'id': ['1', '2'], 'name': ['try1', 'try2'],
                               'full_name': ['full_try1', nan]})[["id", "name", "full_name"]]
    test_result_3 = DataFrame({'id': ['1', '3'], 'name': ['try1', nan],
                               'full_name': ['full_try1', 'full_try3']})[["id", "name", "full_name"]]
    test_result_4 = DataFrame({'id': ['1'], 'full_name_left_side': ['try1'],
                               'full_name_right_side': ['full_try1']})[["full_name_left_side", "id",
                                                                        "full_name_right_side"]]

    transformer = Transformers()

    def test_Transformers_combine(self):
        # inner join
        comb_res1 = self.transformer.combine(self.test_df_1, self.test_df_2, "id", "id")[["id", "name", "full_name"]]
        assert_frame_equal(comb_res1, self.test_result_1)

        # left join
        comb_res2 = self.transformer.combine(self.test_df_1, self.test_df_2, "id", "id","left")[["id", "name",
                                                                                                 "full_name"]]
        assert_frame_equal(comb_res2, self.test_result_2)

        # right join
        comb_res3 = self.transformer.combine(self.test_df_1, self.test_df_2, "id", "id","right")[["id", "name",
                                                                                                 "full_name"]]
        assert_frame_equal(comb_res3, self.test_result_3)

        #suffixes
        comb_res4 = self.transformer.combine(self.test_df_3, self.test_df_2, "id", "id",
                                             suffixes=('_left_side', '_right_side'))
        assert_frame_equal(comb_res4, self.test_result_4)


if __name__ == '__main__':
    unittest.main()
