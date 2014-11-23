__author__ = 'moshebasanchig'

from hydro.exceptions import HydroException


class CacheBase(object):
    """
    Any Cache engine need to implement the following methods
    """
    def get(self, key):
        """
        get a serializable key, return serializable value
        """
        raise HydroException('Not implemented')

    def put(self, key, value, ttl):
        """
        put serializable key and value with ttl(time to live in seconds, 0/-1 - no cache, None-Max tll)
        """
        raise HydroException('Not implemented')
