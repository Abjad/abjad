# -*- encoding: utf-8 -*-
import datetime
import time
from abjad.tools.abctools.AbjadObject import AbjadObject


class IOTranscriptEntry(AbjadObject):
    r'''IO transcript entry.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_current_time',
        '_lines',
        '_terminal_was_cleared',
        )

    ### INITIALIZER ###
    
    def __init__(self, lines, terminal_was_cleared=None):
        assert isinstance(terminal_was_cleared, (bool, type(None)))
        current_time = datetime.datetime.fromtimestamp(time.time())
        self._current_time = current_time
        self._lines = lines[:]
        self._terminal_was_cleared = terminal_was_cleared

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if expr == 0:
            raise Exception
        elif expr in (1, -2):
            return self.lines
        elif expr in (2, -1):
            return self.terminal_was_cleared
        else:
            raise ValueError(expr)

    ### PUBLIC PROPERTIES ###

    @property
    def current_time(self):
        r'''Current time of entry.

        Returns datetime.
        '''
        return self._current_time

    @property
    def lines(self):
        r'''Entry lines.

        Returns list.
        '''
        return self._lines

    @property
    def terminal_was_cleared(self):
        r'''Is true when terminal was cleared. Otherwise false.

        Returns boolean.
        '''
        return self._terminal_was_cleared
