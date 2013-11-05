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

    Returns LilyPond version token.
    '''

    ### INITIALIZER ###

    def __init__(self, version=None):
        assert isinstance(version, (str, type(None)))
        self._version = version

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Get format.

        Return string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, format(self))

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return r'\version "{}"'.format(self.version)

    ### PUBLIC PROPERTIES ###

    @property
    def version(self):
        from abjad import abjad_configuration
        if self._version is None:
            return abjad_configuration.get_lilypond_version_string()
        return self._version
