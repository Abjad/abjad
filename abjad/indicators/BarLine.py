import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class BarLine(AbjadValueObject):
    r"""
    Bar line.

    ..  container:: example

        Final bar line:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> bar_line = abjad.BarLine('|.')
        >>> abjad.attach(bar_line, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> bar_line
        BarLine('|.')

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \bar "|."
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_abbreviation',
        )

    _context = 'Staff'

    _format_slot = 'closing'

    ### INITIALIZER ##

    def __init__(self, abbreviation: str = '|') -> None:
        assert isinstance(abbreviation, str), repr(abbreviation)
        self._abbreviation = abbreviation

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
        bundle.after.commands.append(self._get_lilypond_format())
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

        """
        return self._abbreviation

    @property
    def context(self) -> str:
        r"""
        Gets (historically conventional) context.

        ..  container:: example

            >>> bar_line = abjad.BarLine('|.')
            >>> bar_line.context
            'Staff'

        ..  todo:: Should return ``'Score'``.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on bar line.
        
        The LilyPond ``\bar`` command refuses tweaks.

        Use overrides instead.
        """
        pass
