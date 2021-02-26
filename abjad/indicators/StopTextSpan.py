import typing

from ..bundle import LilyPondFormatBundle
from ..storage import StorageFormatManager


class StopTextSpan:
    r"""
    LilyPond ``\stopTextSpan`` command.

    ..  container:: example

        >>> abjad.StopTextSpan()
        StopTextSpan(command='\\stopTextSpan')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_command", "_leak")

    _context = "Voice"

    _parameter = "TEXT_SPANNER"

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, command: str = r"\stopTextSpan", *, leak: bool = None) -> None:
        assert isinstance(command, str), repr(command)
        assert command.startswith("\\"), repr(command)
        self._command = command
        if leak is not None:
            leak = bool(leak)
        self._leak = leak

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = self.command
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> str:
        """
        Gets command.
        """
        return self._command

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StopTextSpan().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def enchained(self) -> bool:
        """
        Is true.
        """
        return True

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when stop text span leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartTextSpan(
            ...     left_text=abjad.Markup(r"\upright pont."),
            ...     right_text=abjad.Markup(r"\upright tasto"),
            ...     style="dashed-line-with-arrow",
            ...     )
            >>> abjad.tweak(command).staff_padding = 2.5
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTextSpan()
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \abjad-dashed-line-with-arrow
                    - \tweak bound-details.left.text \markup \concat { \upright
                        pont. \hspace #0.5 }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    d'4
                    e'4
                    \stopTextSpan
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartTextSpan(
            ...     left_text=abjad.Markup(r"\upright pont."),
            ...     right_text=abjad.Markup(r"\upright tasto"),
            ...     style="dashed-line-with-arrow",
            ...     )
            >>> abjad.tweak(command).staff_padding = 2.5
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTextSpan(leak=True)
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \abjad-dashed-line-with-arrow
                    - \tweak bound-details.left.text \markup \concat { \upright
                        pont. \hspace #0.5 }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    d'4
                    e'4
                    <> \stopTextSpan
                    r4
                }

        """
        return self._leak

    @property
    def parameter(self) -> str:
        """
        Returns ``'TEXT_SPANNER'``.

        ..  container:: example

            >>> abjad.StopTextSpan().parameter
            'TEXT_SPANNER'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopTextSpan().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_stop(self) -> bool:
        """
        Is true.
        """
        return True
