# -*- encoding: utf-8 -*-
import time
from abjad.tools.abctools import AbjadObject


class DateTimeToken(AbjadObject):
    '''Date / time token.

    ::

        >>> lilypondfiletools.DateTimeToken()
        DateTimeToken(...)

    Returns date / time token.
    '''

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Gets format.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        r'''Interpreter representation of date / time token.

        Returns string.
        '''
        return '{}({})'.format(type(self).__name__, self._lilypond_format)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        current_time_string = time.strftime('%Y-%m-%d %H:%M')
        return current_time_string
