import unittest
from django.conf import settings

__author__ = 'moshebasanchig'


class InMemoryCacheTest(unittest.TestCase):
    def setUp(self):
        if not settings.configured:
            settings.configure()
        # importing in_memory only after django was initialized, otherwise it'll fail
        from hydro.cache.in_memory import InMemoryCache
        self.cache = InMemoryCache()
        self.cache.put('1', [1, 2, 3])

    def test_cache_miss(self):
        data = self.cache.get('2')
        self.assertIsNone(data)

    def test_cache_hit(self):
        data = self.cache.get('1')
        self.assertListEqual(data, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
