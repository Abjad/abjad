import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import format as _format


class StopBeam:
    r"""
    LilyPond ``]`` command.

    ..  container:: example

        >>> abjad.StopBeam()
        StopBeam()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_leak",)

    context = "Voice"
    parameter = "BEAM"
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
        string = "]"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            # bundle.after.spanner_stops.append(string)
            # starts (instead of stops) so [ ] is possible on single leaf:
            bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when stop beam leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'8 d' e' r")
            >>> start_beam = abjad.StartBeam()
            >>> abjad.tweak(start_beam).color = "#blue"
            >>> abjad.attach(start_beam, staff[0])
            >>> stop_beam = abjad.StopBeam()
            >>> abjad.attach(stop_beam, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'8
                    - \tweak color #blue
                    [
                    d'8
                    e'8
                    ]
                    r8
                }

            With leak:

            >>> staff = abjad.Staff("c'8 d' e' r")
            >>> command = abjad.StartBeam()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopBeam(leak=True)
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'8
                    - \tweak color #blue
                    [
                    d'8
                    e'8
                    <> ]
                    r8
                }

        """
        return self._leak
