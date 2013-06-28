from abjad.tools.abctools import AbjadObject
from abjad.tools.configurationtools.get_lilypond_version_string \
	import get_lilypond_version_string


class LilyPondVersionToken(AbjadObject):
    r'''.. versionadded:: 2.0

    LilyPond version token:
    
    ::

        >>> lilypondfiletools.LilyPondVersionToken()
        LilyPondVersionToken(\version "...")

    A specific version can also be specified:

    ::

        >>> f(lilypondfiletools.LilyPondVersionToken('2.16.0'))
        \version "2.16.0"

    Return LilyPond version token.
    '''

    ### INITIALIZER ###

    def __init__(self, version=None):
        assert isinstance(version, (str, type(None)))
        self._version = version

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.lilypond_format)

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''Format contribution of LilyPond version token:

        ::

            >>> lilypondfiletools.LilyPondVersionToken().lilypond_format
            '\\version "..."'

        Return string.
        '''
        return r'\version "{}"'.format(self.version)

    @property
    def version(self):
        if self._version is None:
            return get_lilypond_version_string()
        return self._version
