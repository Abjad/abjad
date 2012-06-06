from abjad.tools import configurationtools
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
        return '{}({!r})'.format(
            self._class_name, configurationtools.read_abjad_user_config_file('lilypond_lang'))

    ### PUBLIC PROPERTIES ###

    @property
    def format(self):
        r'''Format contribution of LilyPond language token::

            >>> lilypondfiletools.LilyPondLanguageToken().format
            '\\language "english"'

        Return string.
        '''
        lilypond_language = configurationtools.read_abjad_user_config_file('lilypond_lang')
        return r'\language "%s"' % lilypond_language.lower()
