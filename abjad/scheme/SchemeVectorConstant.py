import typing
from abjad.system.FormatSpecification import FormatSpecification
from abjad.utilities.String import String
from .Scheme import Scheme


class SchemeVectorConstant(Scheme):
    """
    Abjad model of Scheme vector constant.

    ..  container:: example

        Scheme vector constant of boolean values:

        >>> scheme = abjad.SchemeVectorConstant([True, True, False])
        >>> scheme
        SchemeVectorConstant(True, True, False)
        >>> print(format(scheme))
        #'#(#t #t #f)

    Scheme vectors and Scheme vector constants differ in only their LilyPond
    input format.
    """

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        value: typing.List = [],
        ) -> None:
        Scheme.__init__(self, value, quoting="'#")

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = self._value
        if String.is_string(self._value):
            values = [self._value]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )
