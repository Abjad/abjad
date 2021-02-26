import typing

from .. import enums
from ..bundle import LilyPondFormatBundle
from ..storage import StorageFormatManager


class StopGroup:
    r"""
    LilyPond ``\stopGroup`` command.

    ..  container:: example

        >>> abjad.StopGroup()
        StopGroup()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_leak",)

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
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = r"\stopGroup"
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
        Is true when stop group leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartGroup()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopGroup()
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \startGroup
                    d'4
                    e'4
                    \stopGroup
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartGroup()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopGroup(leak=True)
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \startGroup
                    d'4
                    e'4
                    <> \stopGroup
                    r4
                }

        ..  container:: example

            REGRESSION. Leaked contributions appear last in postevent format
            slot:

            >>> staff = abjad.Staff("c'8 d' e' f' r2")
            >>> abjad.beam(staff[:4])
            >>> command = abjad.StartGroup()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopGroup(leak=True)
            >>> abjad.attach(command, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'8
                    [
                    - \tweak color #blue
                    \startGroup
                    d'8
                    e'8
                    f'8
                    ]
                    <> \stopGroup
                    r2
                }

            The leaked text spanner above does not inadvertantly leak the beam.

        """
        return self._leak

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopGroup().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_stop(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopGroup().spanner_stop
            True

        """
        return True
