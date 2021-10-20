import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import format as _format


class StopTrillSpan:
    r"""
    LilyPond ``\stopTrillSpan`` command.

    ..  container:: example

        >>> abjad.StopTrillSpan()
        StopTrillSpan()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_leak",)

    context = "Voice"
    parameter = "TRILL"
    persistent = True
    spanner_stop = True

    _time_orientation = _enums.Right

    ### INITIALIZER ###

    def __init__(self, *, leak: bool = None) -> None:
        if leak is not None:
            leak = bool(leak)
        self._leak = leak

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Delegates to storage format manager.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = r"\stopTrillSpan"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when stop trill spanner leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartTrillSpan()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTrillSpan()
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \startTrillSpan
                    d'4
                    e'4
                    \stopTrillSpan
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartTrillSpan()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTrillSpan(leak=True)
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \startTrillSpan
                    d'4
                    e'4
                    <> \stopTrillSpan
                    r4
                }

        """
        return self._leak
