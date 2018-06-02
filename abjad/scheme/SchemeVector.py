import typing
from abjad.system.FormatSpecification import FormatSpecification
from abjad.utilities.String import String
from .Scheme import Scheme


class SchemeVector(Scheme):
    """
    Abjad model of Scheme vector.

    ..  container:: example

        Scheme vector of boolean values:

        >>> scheme = abjad.SchemeVector([True, True, False])
        >>> scheme
        SchemeVector(True, True, False)
        >>> print(format(scheme))
        #'(#t #t #f)

    ..  container:: example

        Scheme vector of symbols:

        >>> scheme = abjad.SchemeVector(['foo', 'bar', 'blah'])
        >>> scheme
        SchemeVector('foo', 'bar', 'blah')
        >>> print(format(scheme))
        #'(foo bar blah)

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
        Scheme.__init__(self, value, quoting="'")

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
