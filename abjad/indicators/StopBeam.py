import typing

from .. import enums
from ..bundle import LilyPondFormatBundle
from ..storage import StorageFormatManager


class StopBeam:
    r"""
    LilyPond ``]`` command.

    ..  container:: example

        >>> abjad.StopBeam()
        StopBeam()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_leak",)

    _context = "Voice"

    _parameter = "BEAM"

    _persistent = True

    _time_orientation = enums.Right

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
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
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
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StopBeam().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

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

    @property
    def parameter(self) -> str:
        """
        Returns ``'BEAM'``.

        ..  container:: example

            >>> abjad.StopBeam().parameter
            'BEAM'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopBeam().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_stop(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopBeam().spanner_stop
            True

        """
        return True
