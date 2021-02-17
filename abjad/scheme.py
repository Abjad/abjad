"""
Tools for modeling Scheme datastructures used in LilyPond.
"""

import typing

from .fsv import format_scheme_value
from .storage import FormatSpecification, StorageFormatManager


class Scheme:
    r"""
    Abjad model of Scheme code.

    ..  container:: example

        A Scheme boolean value:

        >>> scheme = abjad.Scheme(True)
        >>> print(abjad.lilypond(scheme))
        ##t

    ..  container:: example

        A nested Scheme expession:

        >>> scheme = abjad.Scheme([
        ...     ('left', (1, 2, False)),
        ...     ('right', (1, 2, 3.3)),
        ...     ])
        >>> print(abjad.lilypond(scheme))
        #((left (1 2 #f)) (right (1 2 3.3)))

    ..  container:: example

        A list:

        >>> scheme_1 = abjad.Scheme([1, 2, 3])
        >>> scheme_2 = abjad.Scheme((1, 2, 3))
        >>> abjad.lilypond(scheme_1) == abjad.lilypond(scheme_2)
        True

        Scheme wraps nested variable-length arguments in a tuple.

    ..  container:: example

        A quoted Scheme expression:

        >>> scheme = abjad.Scheme((1, 2, 3), quoting="'#")
        >>> print(abjad.lilypond(scheme))
        #'#(1 2 3)

        Use the ``quoting`` keyword to prepend Scheme's various quote, unquote,
        unquote-splicing characters to formatted output.

    ..  container:: example

        A Scheme expression with forced quotes:

        >>> scheme = abjad.Scheme('nospaces', force_quotes=True)
        >>> print(abjad.lilypond(scheme))
        #"nospaces"

        Use this in certain \override situations when LilyPond's Scheme
        interpreter treats unquoted strings as symbols instead of strings.
        The string must contain no whitespace for this to work.

    ..  container:: example

        A Scheme lambda expression of LilyPond function that takes a markup
        with a quoted string argument. Setting verbatim to true causes the
        expression to format exactly as-is without modifying quotes or
        whitespace:

        >>> string = '(lambda (grob) (grob-interpret-markup grob'
        >>> string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        >>> scheme = abjad.Scheme(string, verbatim=True)
        >>> print(abjad.storage(scheme))
        abjad.Scheme(
            '(lambda (grob) (grob-interpret-markup grob #{ \\markup \\musicglyph #"noteheads.s0harmonic" #}))',
            verbatim=True,
            )

        >>> print(abjad.lilypond(scheme))
        #(lambda (grob) (grob-interpret-markup grob #{ \markup \musicglyph #"noteheads.s0harmonic" #}))

    ..  container:: example

        More examples:

        >>> abjad.Scheme(True)
        Scheme(True)

        >>> abjad.Scheme(False)
        Scheme(False)

        >>> abjad.Scheme(None)
        Scheme(None)

        >>> abjad.Scheme('hello')
        Scheme('hello')

        >>> abjad.Scheme('hello world')
        Scheme('hello world')

        >>> abjad.Scheme([abjad.Scheme('foo'), abjad.Scheme(3.14159)])
        Scheme([Scheme('foo'), Scheme(3.14159)])

        >>> abjad.Scheme("#'((padding . 1) (attach-dir . -1))")
        Scheme("#'((padding . 1) (attach-dir . -1))")

    ..  container:: example

        Scheme attempts to format Python values into abjad.Scheme equivalents:

        >>> abjad.lilypond(abjad.Scheme(True))
        '##t'

        >>> abjad.lilypond(abjad.Scheme(False))
        '##f'

        >>> abjad.lilypond(abjad.Scheme(None))
        '##f'

        >>> abjad.lilypond(abjad.Scheme('hello world'))
        '#"hello world"'

        >>> abjad.lilypond(abjad.Scheme([1, 2, 3]))
        '#(1 2 3)'

        >>> abjad.lilypond(
        ...     abjad.Scheme(
        ...         "#'((padding . 1) (attach-dir . -1))"
        ...     )
        ... )
        "#'((padding . 1) (attach-dir . -1))"

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_force_quotes", "_quoting", "_value", "_verbatim")

    lilypond_color_constants = (
        "black",
        "blue",
        "center",
        "cyan",
        "darkblue",
        "darkcyan",
        "darkgreen",
        "darkmagenta",
        "darkred",
        "darkyellow",
        "down",
        "green",
        "grey",
        "left",
        "magenta",
        "red",
        "right",
        "up",
        "white",
        "yellow",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        value: typing.Any = None,
        force_quotes: bool = None,
        quoting: str = None,
        verbatim: bool = None,
    ) -> None:
        self._value = value
        if force_quotes is not None:
            force_quotes = bool(force_quotes)
        self._force_quotes = force_quotes
        if quoting is not None and not set(r"',@`#").issuperset(set(quoting)):
            raise ValueError(rf"quoting must be ' or , or @ or ` or #: {quoting!r}.")
        self._quoting = quoting
        if verbatim is not None:
            verbatim = bool(verbatim)
        self._verbatim = verbatim

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.

        Returns true or false.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        """
        Gets string representation of scheme object.
        """
        string = self._get_formatted_value()
        if self.quoting is not None:
            string = self.quoting + string
        return string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.value]
        return FormatSpecification(client=self, storage_format_args_values=values)

    def _get_formatted_value(self):
        return format_scheme_value(
            self.value, force_quotes=self.force_quotes, verbatim=self.verbatim
        )

    def _get_lilypond_format(self):
        string = self._get_formatted_value()
        if self.quoting is not None:
            string = self.quoting + string
        if string in ("#t", "#f") or not string.startswith("#"):
            string = "#" + string
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def force_quotes(self) -> typing.Optional[bool]:
        """
        Is true when quotes should be forced in output.
        """
        return self._force_quotes

    @property
    def quoting(self) -> typing.Optional[str]:
        """
        Gets Scheme quoting string.
        """
        return self._quoting

    @property
    def value(self) -> typing.Any:
        """
        Gets value.
        """
        return self._value

    @property
    def verbatim(self) -> typing.Optional[bool]:
        """
        Is true when formatting should format value absolutely verbatim.
        Whitespace, quotes, and all other parts of value are left intact.
        """
        return self._verbatim
