# -*- encoding: utf-8 -*-
import time
from abjad.tools.abctools import AbjadObject


class DateTimeToken(AbjadObject):
    '''A LilyPond file date / time token.

    ..  container:: example

        >>> lilypondfiletools.DateTimeToken() # doctest: +SKIP
        DateTimeToken('2014-01-04 14:42')

    '''

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats date / time token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.DateTimeToken()
                >>> print format(token) # doctest: +SKIP
                2014-01-04 14:42

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of date / time token.

        ..  container:: example

            ::

                >>> lilypondfiletools.DateTimeToken() # doctest: +SKIP
                DateTimeToken('2014-01-04 14:42')

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._lilypond_format)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        current_time_string = time.strftime('%Y-%m-%d %H:%M')
        return current_time_string
