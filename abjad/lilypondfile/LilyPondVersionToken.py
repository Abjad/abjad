from abjad.system.AbjadObject import AbjadObject


class LilyPondVersionToken(AbjadObject):
    r"""
    A LilyPond file ``\version`` token.

    ..  container:: example

        >>> abjad.LilyPondVersionToken() # doctest: +SKIP
        LilyPondVersionToken('2.19.0')

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_version_string',
        )

    ### INITIALIZER ###

    def __init__(self, version_string=None):
        from abjad import abjad_configuration
        assert isinstance(version_string, (str, type(None)))
        if version_string is None:
            version_string = abjad_configuration.get_lilypond_version_string()
        self._version_string = version_string

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r"""
        Formats LilyPond version token.

        ..  container:: example

            >>> token = abjad.LilyPondVersionToken()
            >>> print(format(token)) # doctest: +SKIP
            \version "2.19.0"

        Return string.
        """
        import abjad
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __repr__(self):
        """
        Gets interpreter representation of LilyPond version_string token.

        ..  container:: example

            >>> token = abjad.LilyPondVersionToken()
            >>> token # doctest: +SKIP
            LilyPondVersionToken('2.19.0')

        Returns string.
        """
        return '{}({!r})'.format(type(self).__name__, self.version_string)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return r'\version "{}"'.format(self.version_string)

    ### PUBLIC PROPERTIES ###

    @property
    def version_string(self):
        """
        Gets version string of LilyPond version token.

        ..  container:: example

            Gets version string from install environment:

            >>> token = abjad.LilyPondVersionToken(
            ...     version_string=None,
            ...     )
            >>> token.version_string # doctest: +SKIP
            '2.19.0'

        ..  container:: example

            Gets version string from explicit input:

            >>> token = abjad.LilyPondVersionToken(
            ...     version_string='2.19.0',
            ...     )
            >>> token.version_string
            '2.19.0'

        Returns string.
        """
        return self._version_string
