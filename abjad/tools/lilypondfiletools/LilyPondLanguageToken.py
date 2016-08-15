# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class LilyPondLanguageToken(AbjadValueObject):
    r'''A LilyPond file ``\language`` token.

    ..  container:: example

        ::

            >>> lilypondfiletools.LilyPondLanguageToken()
            LilyPondLanguageToken()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond language token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.LilyPondLanguageToken()
                >>> print(format(token))
                \language "english"

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of LilyPond language token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.LilyPondLanguageToken()
                >>> token
                LilyPondLanguageToken()

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        string = r'\language "english"'
        return string
