# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondVersionToken(AbjadObject):
    r'''LilyPond version token.
    
    ..  container:: example

        Retrieves version from install environment:

        ::

            >>> lilypondfiletools.LilyPondVersionToken(version=None) # doctest +SKIP
            LilyPondVersionToken(\version "2.18.0")

    ..  container:: example

        Sets version explicitly:

        ::

            >>> lilypondfiletools.LilyPondVersionToken(version='2.19.0')
            LilyPondVersionToken(\version "2.19.0")

    '''

    ### INITIALIZER ###

    def __init__(self, version=None):
        from abjad import abjad_configuration
        assert isinstance(version, (str, type(None)))
        if version is None:
            version = abjad_configuration.get_lilypond_version_string()
        self._version = version

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond version token.

        Return string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of LilyPond version token.

        Returns string.
        '''
        return '{}({})'.format(type(self).__name__, format(self))

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return r'\version "{}"'.format(self.version)

    ### PUBLIC PROPERTIES ###

    @property
    def version(self):
        r'''Version of LilyPond version token.

        ..  container:: example

            ::

                >>> token = lilypondfiletools.LilyPondVersionToken()
                >>> token.version # doctest: +SKIP
                '2.18.0'

        Returns string.
        '''
        return self._version
