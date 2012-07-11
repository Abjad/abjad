from abjad.tools.abctools import AbjadObject
from abjad.tools.configurationtools.get_lilypond_version_string import get_lilypond_version_string


class LilyPondLanguageToken(AbjadObject):
    r'''.. versionadded:: 2.0

    LilyPond language token::

        >>> lilypondfiletools.LilyPondLanguageToken()
        LilyPondLanguageToken('english')

    Return LilyPond language token.

    .. versionchanged:: 2.9
        format with LilyPond ``\language`` command instead of LilyPond ``\include`` command.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __repr__(self):
        from abjad import ABJCFG
        return '{}({!r})'.format(
            self._class_name, ABJCFG['lilypond_language'])

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''Format contribution of LilyPond language token::

            >>> lilypondfiletools.LilyPondLanguageToken().lilypond_format
            '\\language "english"'

        Return string.
        '''
        from abjad import ABJCFG
        lilypond_language = ABJCFG['lilypond_language']
        return r'\language "%s"' % lilypond_language.lower()
