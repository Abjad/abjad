# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject
import time


class DateTimeToken(AbjadObject):
    '''Date time token:

    ::

        >>> lilypondfiletools.DateTimeToken()
        DateTimeToken(...)

    Returns date / time token.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Gets format.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._lilypond_format)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        current_time_string = time.strftime('%Y-%m-%d %H:%M')
        return current_time_string
