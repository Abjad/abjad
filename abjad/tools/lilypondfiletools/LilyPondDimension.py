# -*- encoding: utf-8 -*-
import numbers
from abjad.tools import abctools


class LilyPondDimension(abctools.AbjadObject):
    r'''A LilyPond file ``\paper`` block dimension.

    ..  container:: example

        ::

            >>> lilypondfiletools.LilyPondDimension(2, 'in')
            LilyPondDimension(value=2, unit='in')

    Use for LilyPond file ``\paper`` block attributes.
    '''

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
        r'''Formats LilyPond dimension.

        ..  container:: example

            ::

                >>> dimension = lilypondfiletools.LilyPondDimension(2, 'in')
                >>> print(format(dimension))
                2\in

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return [r'{}\{}'.format(self.value, self.unit)]

    @property
    def _lilypond_format(self):
        return '\n'.join(self._format_pieces)

    ### PUBLIC PROPERTIES ###

    @property
    def unit(self):
        r'''Gets unit of LilyPond dimension.

        ..  container:: example

            ::

                >>> dimension = lilypondfiletools.LilyPondDimension(2, 'in')
                >>> dimension.unit
                'in'

        Returns ``'cm'``, ``'in'``, ``'mm'`` or ``'pt'``.
        '''
        return self._unit

    @property
    def value(self):
        r'''Gets value of LilyPond dimension.

        ..  container:: example

            ::

                >>> dimension = lilypondfiletools.LilyPondDimension(2, 'in')
                >>> dimension.value
                2

        Returns number.
        '''
        return self._value
