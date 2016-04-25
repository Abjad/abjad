# -*- coding: utf-8 -*-
from abjad.tools.schemetools.Scheme import Scheme


class SchemeSymbol(Scheme):
    r'''A Scheme symbol.

    ..  container:: example

        ::

            >>> scheme = schemetools.SchemeSymbol('cross')
            >>> scheme
            SchemeSymbol('cross')

        ::

            >>> print(format(scheme))
            #'cross

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, symbol=None):
        if symbol is None:
            symbol = 'cross'
        symbol = str(symbol)
        Scheme.__init__(
            self,
            symbol,
            quoting="'",
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (self._value,)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def symbol(self):
        r'''Gets symbol string.

        Returns string.
        '''
        return self._value
