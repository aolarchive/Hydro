from hydro.exceptions import HydroException
from datetime import datetime

__author__ = 'moshebasanchig'


class HydroType(object):
    """
    Hydro Type is an abstract class for types that need to be parsed and injected into the queries as filters
    """
    def __init__(self, value, **kwargs):
        self._value = self.parse(value, **kwargs)
        if self._value is None:
            raise HydroException("Value is not set")

    def to_string(self):
        return str(self._value)

    def parse(self, value, kwargs):
        raise HydroException("Not implemented")

    def __sub__(self, other):
        interval = self.value - other.value
        return interval

    @property
    def value(self):
        return self._value


class HydroStr(HydroType):

    def parse(self, value, **kwargs):
        return str(value)


class HydroDatetime(HydroType):
    format = "%Y-%m-%d %H:%M:%S"

    def parse(self, value, **kwargs):
        if 'format' in kwargs:
            self.format = kwargs['format']
        dt = value.split(' ')
        if len(dt) == 1:
            dt.append('00:00:00')
        return datetime.strptime(' '.join(dt), self.format)

    def to_string(self):
        return datetime.strftime(self._value, self.format)


class HydroList(HydroType):
    def parse(self, value, **kwargs):
        if isinstance(value, list):
            return value
        else:
            raise HydroException("Expected a list")

    def to_string(self):
        return ', '.join("'{0}'".format(val) for val in self._value)