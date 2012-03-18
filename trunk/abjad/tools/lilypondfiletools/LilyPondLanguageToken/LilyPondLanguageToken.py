from abjad.cfg._read_config_file import _read_config_file
from abjad.tools.abctools import AbjadObject
from abjad.tools.configurationtools.get_lilypond_version_string import get_lilypond_version_string


class LilyPondLanguageToken(AbjadObject):
    r'''.. versionadded:: 2.0

    LilyPond language token::

        abjad> lilypondfiletools.LilyPondLanguageToken()
        LilyPondLanguageToken(\include "english.ly")

    Return LilyPond language token.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.format)

    ### PUBLIC PROPERTIES ###

    @property
    def format(self):
        r'''Format contribution of LilyPond language token::

            abjad> lilypondfiletools.LilyPondLanguageToken().format
            '\\include "english.ly"'

        Return string.
        '''
        lilypond_language = _read_config_file()['lilypond_lang']
        return r'\include "%s.ly"' % lilypond_language.lower()
