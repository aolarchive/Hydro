import logging
import logging.config
from hydro.conf.settings import APPLICATION_NAME
from hydro.conf.logger import LOGGER_CONFIG

__author__ = 'yanivshalev'


class Logger:
    _logger = None

    @classmethod
    def set_logger(cls, logger):
        cls._logger = logger

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            logging.config.dictConfig(LOGGER_CONFIG)
            cls._logger = logging.getLogger(APPLICATION_NAME)
        return cls._logger


def get_logger():
    return Logger.get_logger()

if __name__ == '__main__':
    def test_func():
        get_logger().debug('ddd')
    test_func()

    class test_class():
        def test_func(self):
            get_logger().debug('ddd')

    test_class().test_func()