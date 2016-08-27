# -*- coding: utf-8 -*-
import time
from abjad.tools.abctools import AbjadObject


class DateTimeToken(AbjadObject):
    '''A LilyPond file date / time token.

    ..  container:: example

        >>> lilypondfiletools.DateTimeToken()
        DateTimeToken()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_date_string',
        )

    ### INITIALIZER ###

    def __init__(self, date_string=None):
        assert isinstance(date_string, (str, type(None)))
        self._date_string = date_string

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats date / time token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.DateTimeToken()
                >>> print(format(token)) # doctest: +SKIP
                2014-01-04 14:42

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of date / time token.

        ..  container:: example

            ::

                >>> lilypondfiletools.DateTimeToken()
                DateTimeToken()

        Returns string.
        '''
        date_string = self._date_string or ''
        return '{}({})'.format(type(self).__name__, date_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return self.date_string

    ### PUBLIC PROPERTIES ###

    @property
    def date_string(self):
        r'''Gets date string of date / time token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.DateTimeToken()
                >>> token.date_string # doctest: +SKIP
                '2014-01-23 12:21'

        Returns string.
        '''
        date_string = self._date_string or time.strftime('%Y-%m-%d %H:%M')
        return date_string
