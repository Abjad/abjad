import time
from abjad.system.AbjadObject import AbjadObject


class DateTimeToken(AbjadObject):
    """
    A LilyPond file date / time token.

    ..  container:: example

        >>> abjad.DateTimeToken()
        DateTimeToken()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_date_string',
        )

    ### INITIALIZER ###

    def __init__(self, date_string=None):
        assert isinstance(date_string, (str, type(None)))
        self._date_string = date_string

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        """
        Formats date / time token.

        ..  container:: example

            >>> token = abjad.DateTimeToken()
            >>> print(format(token)) # doctest: +SKIP
            2014-01-04 14:42

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
        Gets interpreter representation of date / time token.

        ..  container:: example

            >>> abjad.DateTimeToken()
            DateTimeToken()

        Returns string.
        """
        date_string = self._date_string or ''
        return '{}({})'.format(type(self).__name__, date_string)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return self.date_string

    ### PUBLIC PROPERTIES ###

    @property
    def date_string(self):
        """
        Gets date string of date / time token.

        ..  container:: example

            >>> token = abjad.DateTimeToken()
            >>> token.date_string # doctest: +SKIP
            '2014-01-23 12:21'

        Returns string.
        """
        date_string = self._date_string or time.strftime('%Y-%m-%d %H:%M')
        return date_string
