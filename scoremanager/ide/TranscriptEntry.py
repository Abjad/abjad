# -*- encoding: utf-8 -*-
import datetime
import time
from abjad.tools.abctools.AbjadObject import AbjadObject


class TranscriptEntry(AbjadObject):
    r'''Transcript entry.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_current_time',
        '_is_menu',
        '_lines',
        )

    ### INITIALIZER ###

    def __init__(self, lines, is_menu=False):
        current_time = datetime.datetime.fromtimestamp(time.time())
        self._current_time = current_time
        self._is_menu = is_menu
        self._lines = lines[:]

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        r'''Gets line in transcript entry.

        Returns line.
        '''
        return self.lines.__getitem__(expr)

    ### PRIVATE METHODS ###

    def _format(self):
        result = []
        result.append(str(self.current_time))
        for line in self.lines:
            result.append(line)
        return '\n'.join(result)

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r'''Gets contents of transcript entry as a single string.

        Use for tests.
        '''
        return ''.join(self.lines)

    @property
    def current_time(self):
        r'''Gets current time of entry.

        Returns datetime.
        '''
        return self._current_time

    @property
    def is_menu(self):
        r'''Is true when entry is menu. First line will then be menu title.

        Returns boolean.
        '''
        return self._is_menu

    @property
    def lines(self):
        r'''Gets entry lines.

        Returns list.
        '''
        return self._lines