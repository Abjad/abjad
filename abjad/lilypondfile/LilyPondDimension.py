import numbers

from abjad.system.StorageFormatManager import StorageFormatManager


class LilyPondDimension(object):
    r"""
    A LilyPond file ``\paper`` block dimension.

    ..  container:: example

        >>> abjad.LilyPondDimension(2, 'in')
        LilyPondDimension(value=2, unit='in')

    Use for LilyPond file ``\paper`` block attributes.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_unit", "_value")

    ### INITIALIZER ###

    def __init__(self, value=0, unit="cm"):
        assert isinstance(value, numbers.Number) and 0 <= value
        assert unit in ("cm", "in", "mm", "pt")
        self._value = value
        self._unit = unit

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=""):
        r"""
        Formats LilyPond dimension.

        ..  container:: example

            >>> dimension = abjad.LilyPondDimension(2, 'in')
            >>> print(format(dimension))
            2\in

        Returns string.
        """
        if format_specification in ("", "lilypond"):
            return self._get_lilypond_format()
        return StorageFormatManager(self).get_storage_format()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_pieces(self, tag=None):
        return [rf"{self.value}\{self.unit}"]

    def _get_lilypond_format(self):
        return "\n".join(self._get_format_pieces())

    ### PUBLIC PROPERTIES ###

    @property
    def unit(self):
        """
        Gets unit of LilyPond dimension.

        ..  container:: example

            >>> dimension = abjad.LilyPondDimension(2, 'in')
            >>> dimension.unit
            'in'

        Returns ``'cm'``, ``'in'``, ``'mm'`` or ``'pt'``.
        """
        return self._unit

    @property
    def value(self):
        """
        Gets value of LilyPond dimension.

        ..  container:: example

            >>> dimension = abjad.LilyPondDimension(2, 'in')
            >>> dimension.value
            2

        Returns number.
        """
        return self._value
