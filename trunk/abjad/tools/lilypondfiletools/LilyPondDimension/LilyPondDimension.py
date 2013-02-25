from abjad.tools import abctools


class LilyPondDimension(abctools.AbjadObject):
    r'''Abjad model of page dimensions in LilyPond:

    ::

        >>> dimension = lilypondfiletools.LilyPondDimension(2, 'in')

    ::

        >>> f(dimension)
        2.0\in

    Return LilyPondDimension instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_unit', '_value')

    ### INITIALIZER ###

    def __init__(self, value, unit):
        assert 0 <= value
        assert unit in ('cm', 'in', 'mm')
        self._value = float(value)
        self._unit = unit

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return [r'{}\{}'.format(self.value, self.unit)]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        return '\n'.join(self._format_pieces)

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value
