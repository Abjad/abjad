from abjad.system.AbjadValueObject import AbjadValueObject


class LilyPondLanguageToken(AbjadValueObject):
    r"""
    A LilyPond file ``\language`` token.

    ..  container:: example

        >>> abjad.LilyPondLanguageToken()
        LilyPondLanguageToken()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r"""
        Formats LilyPond language token.

        ..  container:: example

            >>> token = abjad.LilyPondLanguageToken()
            >>> print(format(token))
            \language "english"

        Returns string.
        """
        import abjad
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __repr__(self):
        """
        Gets interpreter representation of LilyPond language token.

        ..  container:: example

            >>> token = abjad.LilyPondLanguageToken()
            >>> token
            LilyPondLanguageToken()

        Returns string.
        """
        return '{}()'.format(type(self).__name__)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        string = r'\language "english"'
        return string
