# -*- encoding: utf-8 -*-
import time
from abjad.tools.abctools import ContextManager


class Timer(ContextManager):
    r'''A timing context manager:

    ::

        >>> timer = systemtools.Timer()
        >>> with timer:
        ...     for _ in xrange(1000000):
        ...         x = 1 + 1
        ...
        >>> timer.elapsed_time # doctest: +SKIP
        0.092742919921875

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_time',
        '_stop_time',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._start_time = None
        self._stop_time = None

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager.

        Returns none.
        '''
        self._stop_time = None
        self._start_time = time.time()

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exist context manager.

        Returns none.
        '''
        self._stop_time = time.time()

    ### PUBLIC PROPERTIES ###

    @property
    def elapsed_time(self):
        r'''Elapsed time.

        Return float or none.
        '''
        if self.stop_time is not None and self.start_time is not None:
            return self.stop_time - self.start_time
        return None

    @property
    def start_time(self):
        r'''Start time of timer.

        Returns time.
        '''
        return self._start_time

    @property
    def stop_time(self):
        r'''Stop time of timer.

        Returns time.
        '''
        return self._stop_time
