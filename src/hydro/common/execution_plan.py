
__author__ = 'moshebasanchig'
from datetime import datetime
from json import dumps

now = lambda: int(datetime.utcnow().strftime("%s"))


class ExecutionPhase(object):
    def __init__(self, id, phase_name, phase_type, metadata=None, timestamp=None):
        self._id = id
        self._phase_name = phase_name
        self._phase_type = phase_type
        self._metadata = metadata
        if timestamp is None:
            timestamp = now()
        self._timestamp = timestamp

    def to_string(self):
        return dumps({'id': self._id,
                      'phase_name': self._phase_name,
                      'phase_type': self._phase_type,
                      'metadata': self._metadata if self._metadata else "",
                      'timestamp': self._timestamp})

    @property
    def phase_name(self):
        return self._phase_name

    @property
    def phase_type(self):
        return self._phase_type

    @property
    def metadata(self):
        return self._metadata

    @property
    def timestamp(self):
        return self._timestamp


class ExecutionPlan(object):
    def __init__(self):
        self._phases = list()
        self._cntr = 0

    def add_phase(self, cls, phase_name, metadata=None):
        self._phases.append(ExecutionPhase(self._cntr, phase_name, cls.__class__.__name__, metadata, now()))
        self._cntr += 1

    def __iter__(self):
        for phase in self._phases:
            yield phase

    def to_string(self):
        return "\n".join([p.to_string() for p in self.__iter__()])

