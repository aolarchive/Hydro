__author__ = 'yanivshalev'

import unittest
from hydro.common.execution_plan import ExecutionPlan


class ExecutionPlanTest(unittest.TestCase):

    def test_add_phase(self):
        ep = ExecutionPlan()
        #cls must be provided as a first argument in order to track who call it
        ep.add_phase(ExecutionPlan, 'test_phase1', metadata={'test_key1': 'test_val1'})
        ep.add_phase(ExecutionPlan, 'test_phase2', metadata={'test_key2': 'test_val2'})
        phase1, phase2 = ep
        self.assertEquals(phase1.phase_name,'test_phase1')
        self.assertEquals(phase1.metadata,{'test_key1': 'test_val1'})
        self.assertEquals(phase1.phase_type,'type')
        self.assertEquals(phase1._id,0)

        self.assertEquals(phase2.phase_name,'test_phase2')
        self.assertEquals(phase2.metadata,{'test_key2': 'test_val2'})
        self.assertEquals(phase2.phase_type,'type')
        self.assertEquals(phase2._id,1)

        val = eval('['+ep.to_string().replace('\n',',')+']')
        #need to change the timestamp
        val[0]['timestamp']=0
        val[1]['timestamp']=0
        to_comp = [{'timestamp': 0, 'phase_type': 'type', 'phase_name': 'test_phase1', 'id': 0, 'metadata': {'test_key1': 'test_val1'}}, {'timestamp': 0, 'phase_type': 'type', 'phase_name': 'test_phase2', 'id': 1, 'metadata': {'test_key2': 'test_val2'}}]

        self.assertEquals(val, to_comp)


if __name__ == '__main__':
    unittest.main()