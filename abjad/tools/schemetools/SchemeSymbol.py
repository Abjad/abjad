from abjad.tools import systemtools
from abjad.tools.schemetools.Scheme import Scheme


class SchemeSymbol(Scheme):
    r'''Abjad model of Scheme symbol.

    ..  container:: example

        >>> scheme = abjad.SchemeSymbol('cross')
        >>> scheme
        SchemeSymbol('cross')

        >>> print(format(scheme))
        #'cross

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, symbol='cross'):
        symbol = str(symbol)
        Scheme.__init__(self, value=symbol, quoting="'")

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.symbol]
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
