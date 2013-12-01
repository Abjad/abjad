# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondLanguageToken(AbjadObject):
    r'''LilyPond language token.

    ::

        >>> lilypondfiletools.LilyPondLanguageToken()
        LilyPondLanguageToken('english')

    '''

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond language token.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)


    def __repr__(self):
        r'''Interpreter representation of LilyPond language token.

        Returns string.
        '''
        from abjad import abjad_configuration
        return '{}({!r})'.format(
            type(self).__name__, 
            abjad_configuration['lilypond_language'],
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        from abjad import abjad_configuration
        lilypond_language = abjad_configuration['lilypond_language']
        return r'\language "%s"' % lilypond_language.lower()
