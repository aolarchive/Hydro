import unittest
import os
import inspect
from hydro.base_classes import HydroStr, HydroDatetime, Base, HydroCommandTemplate, HydroDatetime, HydroList,\
    PlanObject, Configurator, HydroDataframe
from pandas import DataFrame as df
from datetime import datetime

__author__ = 'yanivshalev'


class BaseClassesTest(unittest.TestCase):
    # params for query/command for creating data streams
    params = {
        'FROM_DATE': '2014-07-01',
        'TO_DATE': '2014-07-31',
        'CLIENT_ID': 'some_client',
        'OBJECT_TYPES': ['obj1', 'obj2']
        }
    # registration of the allowed parameters and their types
    conf = Configurator.config_builder()
    conf.PLAN_ALLOWED_PARAMETERS = {'CLIENT_ID': {'type': HydroStr},
                                    'FROM_DATE': {'type': HydroDatetime},
                                    'TO_DATE': {'type': HydroDatetime},
                                    'OBJECT_TYPES': {'type': HydroList, 'optional': True}
                                    }

    def test_hydro_str(self):
        self.assertEquals(HydroStr(1).to_string(), '1')
        self.assertEquals(HydroStr('1').to_string(), '1')
        self.assertEquals(HydroStr(1).parse('a'), 'a')
        self.assertEquals(HydroStr(1).parse(1), '1')
        self.assertEquals(HydroStr(1).value, '1')

    def test_hydro_datetime(self):
        self.assertNotEqual(HydroDatetime('2014-07-01').to_string(), '1')
        self.assertEqual(HydroDatetime('2014-07-01').to_string(), '2014-07-01 00:00:00')
        self.assertEqual(HydroDatetime('2014-07-01').value, datetime(2014, 7, 1, 0, 0))
        self.assertEqual(HydroDatetime('2014-07-01 07:07:07').value, datetime(2014, 7, 1, 7, 7, 7))
        self.assertNotEqual(HydroDatetime('2014-07-01 07:07:07').value, datetime(2014, 1, 7, 7, 7, 6))
        self.assertEqual(HydroDatetime('2014-07-01 07:07:07').to_string(), '2014-07-01 07:07:07')

    def test_hydrobaseclass(self):
        inst = Base()
        self.assertTrue(hasattr(inst, 'logger'), "Base doesn't contain logger")
        self.assertTrue(hasattr(inst, 'stats'), "Base doesn't contain logger")

    def param_parser(self, params):
        parsed = dict([[x,self.conf.PLAN_ALLOWED_PARAMETERS[x]['type'](params[x])] for x in params])
        return parsed

    def test_hydrocommandtemplate(self):
        sql = """\n            SELECT A,B,C,D,E,F, SUM(M1)\n            FROM TEST_TB\n            WHERE\n            client = 'some_client'\n            AND DATE BETWEEN '2014-07-01 00:00:00' AND '2014-07-31 00:00:00'\n            AND object_type NOT IN ('all objects')\n            AND object_type IN ('obj1', 'obj2')\n            GROUP BY\n            1, 2, 3, 4, 5, 6\n"""
        current_dir = os.path.dirname(inspect.getabsfile(self.__class__))
        inst = HydroCommandTemplate(current_dir, 'test_query.sql')
        cmd = inst.parse(self.param_parser(self.params))
        self.assertEquals(cmd, sql)

    def test_planobject(self):
        inst = PlanObject(self.params, '.', self.conf)
        # checking if members exist
        self.assertTrue(hasattr(inst, 'template_file'), "Base doesn't contain template_file")
        self.assertTrue(hasattr(inst, 'data_source'), "Base doesn't contain data_source")
        self.assertTrue(hasattr(inst, 'source_type'), "Base doesn't contain source_type")
        self.assertTrue(hasattr(inst, 'sampling'), "Base doesn't contain sampling")
        inst.gather_statistics('device_grid_widget', 'ALL')
        for stat in Configurator.OPTIMIZER_STATISTICS['ALL']:
            self.assertTrue(hasattr(inst, stat), "Base doesn't contain {0}".format(stat))

    def test_hydro_dataframe(self):
        data = df({'a': [2, 3], 'b': [7, 8]})
        hdf = HydroDataframe(data).to_string()
        expected_result = 'a, b'
        self.assertEquals(hdf, expected_result)
        # self.assertEquals(HydroStr('1').to_string(), '1')
        # self.assertEquals(HydroStr(1).parse('a'), 'a')
        # self.assertEquals(HydroStr(1).parse(1), '1')
        # self.assertEquals(HydroStr(1).value, '1')


if __name__ == '__main__':
    unittest.main()
