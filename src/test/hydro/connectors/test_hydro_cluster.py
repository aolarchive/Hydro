__author__ = 'moshebasanchig'

import unittest
from hydro.hydro_cluster import LocalHydro
from hydro.exceptions import HydroException


class LocalHydroTest(unittest.TestCase):
    def test_require_topology_instance(self):
        local_hydro = LocalHydro()
        self.assertRaises(HydroException, local_hydro.register, 'not-a-topology', None)


if __name__ == '__main__':
    unittest.main()
