from ..bundle import LilyPondFormatBundle
from ..storage import FormatSpecification, StorageFormatManager


class BarLine:
    r"""
    Bar line.

    ..  container:: example

        Final bar line:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> bar_line = abjad.BarLine("|.")
        >>> abjad.attach(bar_line, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> bar_line
        BarLine('|.', format_slot='after')

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \bar "|."
            }

    ..  container:: example

        Specify repeat bars like this:

        >>> staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")
        >>> abjad.attach(abjad.BarLine(".|:"), staff[3])
        >>> abjad.attach(abjad.BarLine(":|."), staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \bar ".|:"
                g'4
                a'4
                b'4
                c''4
                \bar ":|."
            }

        This allows you to bypass LilyPond's ``\volta`` command.

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_abbreviation", "_format_slot")

    _context = "Score"

    # scraped from LilyPond docs because LilyPond fails to error
    # on unrecognized string
    _known_abbreviations = (
        "",
        "|",
        ".",
        "||",
        ".|",
        "..",
        "|.|",
        "|.",
        ";",
        "!",
        ".|:",
        ":..:",
        ":|.|:",
        ":|.:",
        ":.|.:",
        "[|:",
        ":|][|:",
        ":|]",
        ":|.",
        "'",
    )

    ### INITIALIZER ##

    def __init__(self, abbreviation: str = "|", *, format_slot: str = "after") -> None:
        if abbreviation not in self._known_abbreviations:
            message = f"unknown bar line abbreviation: {repr(abbreviation)}\n"
            message += "Abbreviation must be one of these:\n"
            string = "\n    ".join([repr(_) for _ in self._known_abbreviations])
            message += string
            raise Exception(message)
        self._abbreviation = abbreviation
        assert isinstance(format_slot, str), repr(format_slot)
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Delegates to storage format manager.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            storage_format_is_indented=False,
            storage_format_args_values=[self.abbreviation],
        )

    def _get_lilypond_format(self):
        return rf'\bar "{self.abbreviation}"'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.append(self._get_lilypond_format())
        return bundle

    ## PUBLIC PROPERTIES ##

    @property
    def abbreviation(self) -> str:
        r"""
        Gets abbreviation.

        ..  container:: example

            >>> bar_line = abjad.BarLine('|.')
            >>> bar_line.abbreviation
            '|.'

        ..  container:: example exception:

            Abbreviation error-checking looks like this:

            >>> abjad.BarLine("text")
            Traceback (most recent call last):
                ...
            Exception: unknown bar line abbreviation: 'text'
            Abbreviation must be one of these:
                ''
                '|'
                '.'
                '||'
                '.|'
                '..'
                '|.|'
                '|.'
                ';'
                '!'
                '.|:'
                ':..:'
                ':|.|:'
                ':|.:'
                ':.|.:'
                '[|:'
                ':|][|:'
                ':|]'
                ':|.'
                "'"

        """
        return self._abbreviation

    @property
    def context(self) -> str:
        r"""
        Gets (historically conventional) context.

        ..  container:: example

            >>> bar_line = abjad.BarLine('|.')
            >>> bar_line.context
            'Score'

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def format_slot(self) -> str:
        r"""
        Gets format slot.

        ..  container:: example

            >>> abjad.BarLine("|").format_slot
            'after'

            >>> abjad.BarLine("|", format_slot="before").format_slot
            'before'

        ..  container:: example

            REGRESSION. You can attach a before barline and after barline to
            the same leaf:

            >>> staff = abjad.Staff("c'1 d'1")
            >>> bar_line_1 = abjad.BarLine(".|:", format_slot="before")
            >>> bar_line_2 = abjad.BarLine(":|.", format_slot="after")
            >>> assert bar_line_1.format_slot != bar_line_2.format_slot
            >>> abjad.attach(bar_line_1, staff[-1])
            >>> abjad.attach(bar_line_2, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'1
                    \bar ".|:"
                    d'1
                    \bar ":|."
                }

        """
        return self._format_slot

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on bar line.

        The LilyPond ``\bar`` command refuses tweaks.

        Use overrides instead.
        """
        pass
