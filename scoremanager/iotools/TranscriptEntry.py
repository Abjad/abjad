# -*- encoding: utf-8 -*-
import datetime
import time
from abjad.tools.abctools.AbjadObject import AbjadObject


class TranscriptEntry(AbjadObject):
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

    ### PRIVATE METHODS ###

    def _format(self):
        result = []
        result.append(str(self.current_time))
        if self.terminal_was_cleared:
            result.append('terminal_was_cleared=True')
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
    def terminal_was_cleared(self):
        r'''Is true when terminal was cleared. Otherwise false.

        Returns boolean.
        '''
        return self._terminal_was_cleared

    @property
    def title(self):
        r'''Gets title of entry.

        Returns string.
        '''
        return self.lines[0]
