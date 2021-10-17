import dataclasses

from .. import bundle as _bundle
from .. import format as _format


@dataclasses.dataclass
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
        BarLine(abbreviation='|.', format_slot='after')

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

    abbreviation: str = "|"
    format_slot: str = "after"

    _is_dataclass = True

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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return _format.FormatSpecification(
            storage_format_is_not_indented=True,
            storage_format_args_values=[self.abbreviation],
        )

    def _get_lilypond_format(self):
        return rf'\bar "{self.abbreviation}"'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.append(self._get_lilypond_format())
        return bundle

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
