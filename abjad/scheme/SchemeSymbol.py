from abjad.system.FormatSpecification import FormatSpecification
from .Scheme import Scheme


class SchemeSymbol(Scheme):
    """
    Abjad model of Scheme symbol.

    ..  container:: example

        >>> scheme = abjad.SchemeSymbol('cross')
        >>> scheme
        SchemeSymbol('cross')

        >>> print(format(scheme))
        #'cross

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        symbol: str = 'cross',
        ) -> None:
        symbol = str(symbol)
        Scheme.__init__(self, value=symbol, quoting="'")

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.symbol]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def symbol(self) -> str:
        """
        Gets symbol string.
        """
        assert isinstance(self.value, str)
        return self.value
