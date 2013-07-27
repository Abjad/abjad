from abjad.tools.abctools import AbjadObject


class LilyPondLanguageToken(AbjadObject):
    r'''.. versionadded:: 2.0

    LilyPond language token:

    ::

        >>> lilypondfiletools.LilyPondLanguageToken()
        LilyPondLanguageToken('english')

    Return LilyPond language token.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __repr__(self):
        from abjad import abjad_configuration
        return '{}({!r})'.format(
            self._class_name, abjad_configuration['lilypond_language'])

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''Format contribution of LilyPond language token:

        ::

            >>> lilypondfiletools.LilyPondLanguageToken().lilypond_format
            '\\language "english"'

        Return string.
        '''
        from abjad import abjad_configuration
        lilypond_language = abjad_configuration['lilypond_language']
        return r'\language "%s"' % lilypond_language.lower()
