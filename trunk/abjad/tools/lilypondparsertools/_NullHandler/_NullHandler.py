import logging


class _NullHandler(logging.Handler):
    '''For Python 2.6 compatibility.'''
    def emit(self, record):
        pass
