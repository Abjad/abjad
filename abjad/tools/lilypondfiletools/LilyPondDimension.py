# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class LilyPondDimension(abctools.AbjadObject):
    r'''A LilyPond page dimension.

    ::

        >>> dimension = lilypondfiletools.LilyPondDimension(2, 'in')

    ..  doctest::

        >>> print format(dimension)
        2.0\in

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_unit', 
        '_value',
        )

    ### INITIALIZER ###

    def __init__(self, value=0, unit='cm'):
        assert 0 <= value
        assert unit in ('cm', 'in', 'mm')
        self._value = float(value)
        self._unit = unit

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond dimension.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return [r'{}\{}'.format(self.value, self.unit)]

    ### PUBLIC PROPERTIES ###

    @property
    def _lilypond_format(self):
        return '\n'.join(self._format_pieces)

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value
