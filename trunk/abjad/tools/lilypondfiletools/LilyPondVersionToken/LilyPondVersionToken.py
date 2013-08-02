# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondVersionToken(AbjadObject):
    r'''LilyPond version token:
    
    ::

        >>> lilypondfiletools.LilyPondVersionToken()
        LilyPondVersionToken(\version "...")

    A specific version can also be specified:

    ..  doctest::

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
        return '{}({})'.format(self._class_name, self.lilypond_format)

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
        from abjad import abjad_configuration
        if self._version is None:
            return abjad_configuration.get_lilypond_version_string()
        return self._version
