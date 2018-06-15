import numbers
from abjad import system


class LilyPondDimension(system.AbjadObject):
    r"""
    A LilyPond file ``\paper`` block dimension.

    ..  container:: example

        >>> abjad.LilyPondDimension(2, 'in')
        LilyPondDimension(value=2, unit='in')

    Use for LilyPond file ``\paper`` block attributes.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_unit',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(self, value=0, unit='cm'):
        assert isinstance(value, numbers.Number) and 0 <= value
        assert unit in ('cm', 'in', 'mm', 'pt')
        self._value = value
        self._unit = unit

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r"""
        Formats LilyPond dimension.

        ..  container:: example

            >>> dimension = abjad.LilyPondDimension(2, 'in')
            >>> print(format(dimension))
            2\in

        Returns string.
        """
        import abjad
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        return [r'{}\{}'.format(self.value, self.unit)]

    def _get_lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

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
