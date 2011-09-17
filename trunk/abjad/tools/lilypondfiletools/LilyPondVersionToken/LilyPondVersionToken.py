from abjad.core import _Immutable
from abjad.tools.configurationtools.get_lilypond_version_string import get_lilypond_version_string


class LilyPondVersionToken(_Immutable):
    r'''.. versionadded:: 2.0

    LilyPond version token::

        abjad> lilypondfiletools.LilyPondVersionToken()
        LilyPondVersionToken(\version "...")

    Return LilyPond version token.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.format)

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        r'''Format contribution of LilyPond version token::

            abjad> lilypondfiletools.LilyPondVersionToken().format
            '\\version "..."'

        Return string.
        '''
        return r'\version "%s"' % get_lilypond_version_string()
