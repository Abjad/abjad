from abjad.system.StorageFormatManager import StorageFormatManager


class LilyPondLanguageToken(object):
    r"""
    A LilyPond file ``\language`` token.

    ..  container:: example

        >>> abjad.LilyPondLanguageToken()
        LilyPondLanguageToken()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=""):
        r"""
        Formats LilyPond language token.

        ..  container:: example

            >>> token = abjad.LilyPondLanguageToken()
            >>> print(format(token))
            \language "english"

        Returns string.
        """
        if format_specification in ("", "lilypond"):
            return self._get_lilypond_format()
        return StorageFormatManager(self).get_storage_format()

    def __repr__(self):
        """
        Gets interpreter representation of LilyPond language token.

        ..  container:: example

            >>> token = abjad.LilyPondLanguageToken()
            >>> token
            LilyPondLanguageToken()

        Returns string.
        """
        return f"{type(self).__name__}()"

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        string = r'\language "english"'
        return string
