import typing
from abjad.system.FormatSpecification import FormatSpecification
from .Scheme import Scheme


class SchemePair(Scheme):
    r"""
    Abjad model of Scheme pair.

    ..  container:: example

        Initializes from two values:

        >>> abjad.SchemePair(('spacing', 4))
        SchemePair(('spacing', 4))

    ..  container:: example

        Regression tests:

        Right-hand side string forces quotes:

        >>> scheme_pair = abjad.SchemePair(('font-name', 'Times'))
        >>> format(scheme_pair)
        '#\'(font-name . "Times")'

        Right-hand side nonstring does not force quotes:

        >>> scheme_pair = abjad.SchemePair(('spacing', 4))
        >>> format(scheme_pair)
        "#'(spacing . 4)"

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_value',
        )

    ### INITIALIZER ##

    def __init__(
        self,
        value = (None, None),
        ) -> None:
        assert isinstance(value, tuple), repr(value)
        assert len(value) == 2, repr(value)
        Scheme.__init__(self, value=value)

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        """
        Formats Scheme pair.

        ..  container:: example

            >>> scheme_pair = abjad.SchemePair((-1, 1))

            >>> format(scheme_pair)
            "#'(-1 . 1)"

            >>> abjad.f(scheme_pair)
            abjad.SchemePair((-1, 1))

        """
        return super(SchemePair, self).__format__(
            format_specification=format_specification,
            )

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.value]
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    def _get_formatted_value(self):
        assert len(self._value) == 2
        lhs = Scheme.format_scheme_value(self._value[0])
        # need to force quotes around pairs like
        # \override #'(font-name . "Times")
        rhs = Scheme.format_scheme_value(
            self._value[-1],
            force_quotes=True,
            )
        return f'({lhs} . {rhs})'

    def _get_lilypond_format(self):
        string = self._get_formatted_value()
        return f"#'{string}"

    ### PUBLIC PROPERTIES ###

    @property
    def left(self) -> typing.Any:
        """
        Gets left value.
        """
        pair = self.value
        assert isinstance(pair, tuple)
        return pair[0]

    @property
    def right(self) -> typing.Any:
        """
        Gets right value.
        """
        pair = self.value
        assert isinstance(pair, tuple)
        return pair[-1]
