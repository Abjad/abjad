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
        '_lines',
        )

    ### INITIALIZER ###

    def __init__(self, lines):
        current_time = datetime.datetime.fromtimestamp(time.time())
        self._current_time = current_time
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
    def current_time(self):
        r'''Gets current time of entry.

        Returns datetime.
        '''
        return self._current_time

    @property
    def is_system_display(self):
        r'''Is true when entry is system display. Otherwise false.

        Returns boolean.
        '''
        return not self.is_user_input

    @property
    def is_user_input(self):
        r'''Is true when entry is user input. Otherwise false.

        Returns boolean.
        '''
        return self.lines and '>' in self.lines[0]

    @property
    def lines(self):
        r'''Gets entry lines.

        Returns list.
        '''
        return self._lines

    @property
    def title(self):
        r'''Gets title of entry.

        Returns string.
        '''
        return self.lines[0]