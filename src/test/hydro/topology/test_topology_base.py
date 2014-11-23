__author__ = 'yanivshalev'
import unittest
from hydro.topology_base import Topology


class TP(Topology):
    def _submit(self, params):
        return {'a': 1}


class TestTopologyBase(unittest.TestCase):
    def test_init(self):
        #instanciating a topology
        inst = TP()
        self.assertTrue(hasattr(inst, 'cache_engines'), "Base doesn't contain cache_engines")
        self.assertTrue(hasattr(inst, 'transformers'), "Base doesn't contain transformers")
        self.assertTrue(hasattr(inst, '_templates_dir'), "Base doesn't contain _templates_dir")
        self.assertTrue(hasattr(inst, '_modules_dir'), "Base doesn't contain _modules_dir")
        self.assertTrue(hasattr(inst, '_execution_plan'), "Base doesn't contain _execution_plan")
        self.assertTrue(hasattr(inst, 'query_engine'), "Base doesn't contain query_engine")
        self.assertTrue(hasattr(inst, 'logger'), "Base doesn't contain logger")

    def test_submit(self):
        inst = TP()
        res = inst.submit({})
        self.assertEqual(res, {'a': 1})

    def test_not_implemented(self):
        class TP2(Topology):
            pass
        inst = TP2()
        self.assertRaises(Exception, inst.submit, {})

    def test_topology_caching1(self):
        class TP2(Topology):
            def _submit(self, params):
                return {'a': 1}

        inst = TP2()
        for x in range(10):
            inst.submit({})
        cntr = 0
        for plan in inst.get_execution_plan():
            if cntr == 0:
                self.assertFalse(plan.metadata['topology_cache_hit'])
            else:
                self.assertTrue(plan.metadata['topology_cache_hit'])
            cntr += 1

    def test_topology_caching2(self):
        class TP2(Topology):
            def _submit(self, params):
                return {'a': 1}

        inst = TP2()
        for x in range(10):
            inst.submit({'CLIENT_ID': 'cli'})
        cntr = 0
        for plan in inst.get_execution_plan():
            if cntr == 0:
                self.assertFalse(plan.metadata['topology_cache_hit'])
            else:
                self.assertTrue(plan.metadata['topology_cache_hit'])
            cntr+=1

    def test_topology_caching3(self):
        class TP2(Topology):
            def _submit(self, params):
                return {'a': 1}

        inst = TP2()
        for x in range(10):
            inst.submit({'CLIENT_ID': 'cli'+str(x)})

        #caching is based on topology name name and parameters
        for plan in inst.get_execution_plan():
            self.assertFalse(plan.metadata['topology_cache_hit'])


if __name__ == '__main__':
    unittest.main()
