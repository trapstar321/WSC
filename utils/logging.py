import logging
import traceback
import sys

class ConsoleLogger(object):
    def __init__(self, name, format='%(asctime)s %(levelname)s %(name)s %(func)s()-> %(message)s', datefmt='%d-%m-%Y %H:%M:%S'):
        #logging.basicConfig(format=format)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter(format)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def _extra(self):
        return {'func': sys._getframe(2).f_code.co_name}

    def info(self, msg):
        self.logger.info(msg, extra=self._extra())

    def warning(self, msg):
        self.logger.warning(msg, extra=self._extra())

    def debug(self, msg):
        self.logger.debug(msg, extra=self._extra())

    def error(self, msg):
        self.logger.error(msg, extra=self._extra())

    def log_exception(self):
        self.logger.error(traceback.format_exc(), extra=self._extra())

