__author__ = 'moshebasanchig'


class HydroException(Exception):
    def __init__(self, message, errors=None):
        Exception.__init__(self, message)

        # errors could be a dict that is passed along and will contain extra stuff that can be used to enrich the
        # exception. it'll also be accessible from e.errors when catching the exception.
        self.errors = errors
