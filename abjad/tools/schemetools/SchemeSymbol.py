# -*- coding: utf-8 -*-
from abjad.tools import systemtools
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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self._value]
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def symbol(self):
        r'''Gets symbol string.

        Returns string.
        '''
        return self._value
