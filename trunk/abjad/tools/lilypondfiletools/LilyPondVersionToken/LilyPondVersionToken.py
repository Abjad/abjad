from abjad.tools.abctools import AbjadObject
from abjad.tools.configurationtools.get_lilypond_version_string import get_lilypond_version_string


class LilyPondVersionToken(AbjadObject):
    r'''.. versionadded:: 2.0

    LilyPond version token::

        >>> lilypondfiletools.LilyPondVersionToken()
        LilyPondVersionToken(\version "...")

    Return LilyPond version token.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.lilypond_format)

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''Format contribution of LilyPond version token::

            >>> lilypondfiletools.LilyPondVersionToken().lilypond_format
            '\\version "..."'

        Return string.
        '''
        return r'\version "%s"' % get_lilypond_version_string()
