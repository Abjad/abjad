# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondLanguageToken(AbjadObject):
    r'''A LilyPond language token.

    ..  container:: example

        ::

            >>> lilypondfiletools.LilyPondLanguageToken()
            LilyPondLanguageToken('english')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lilypond_language',
        )

    ### INITIALIZER ###

    def __init__(self):
        from abjad import abjad_configuration
        lilypond_language = abjad_configuration['lilypond_language']
        self._lilypond_language = lilypond_language

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond language token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.LilyPondLanguageToken()
                >>> print format(token)
                \language "english"

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)


    def __repr__(self):
        r'''Gets interpreter representation of LilyPond language token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.LilyPondLanguageToken()
                >>> token
                LilyPondLanguageToken('english')

        Returns string.
        '''
        return '{}({!r})'.format(
            type(self).__name__, 
            self._lilypond_language,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        lilypond_language = self._lilypond_language.lower()
        string = r'\language "{}"'.format(lilypond_language)
        return string
