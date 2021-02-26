import typing

from .. import enums
from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..storage import StorageFormatManager


class StopPianoPedal:
    r"""
    LilyPond ``\sostenutoOff``, ``\sustainOff``, ``\treCorde`` commands.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_kind", "_leak", "_tweaks")

    _context = "StaffGroup"

    _parameter = "PEDAL"

    _persistent = True

    _time_orientation = enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        kind: str = None,
        *,
        leak: bool = None,
        tweaks: TweakInterface = None,
    ) -> None:
        if kind is not None:
            assert kind in ("sustain", "sostenuto", "corda")
        self._kind = kind
        if leak is not None:
            leak = bool(leak)
        self._leak = leak
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        strings = []
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            strings.extend(tweaks)
            # bundle.after.spanner_stops.extend(tweaks)
        if self.kind == "corda":
            string = r"\treCorde"
        elif self.kind == "sostenuto":
            string = r"\sostenutoOff"
        else:
            assert self.kind in ("sustain", None)
            string = r"\sustainOff"
        strings.append(string)
        if self.leak:
            strings.insert(0, "<>")
            bundle.after.leaks.extend(strings)
        else:
            bundle.after.spanner_stops.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'StaffGroup'``.

        ..  container:: example

            >>> abjad.StopPianoPedal().context
            'StaffGroup'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def kind(self) -> typing.Optional[str]:
        """
        Gets kind.
        """
        return self._kind

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when piano pedal stop leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> start_piano_pedal = abjad.StartPianoPedal()
            >>> abjad.tweak(start_piano_pedal).color = "#blue"
            >>> abjad.tweak(start_piano_pedal).parent_alignment_X = abjad.Center
            >>> abjad.attach(start_piano_pedal, staff[0])
            >>> stop_piano_pedal = abjad.StopPianoPedal()
            >>> abjad.tweak(stop_piano_pedal).color = "#red"
            >>> abjad.tweak(stop_piano_pedal).parent_alignment_X = abjad.Center
            >>> abjad.attach(stop_piano_pedal, staff[-2])
            >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override SustainPedalLineSpanner.staff-padding = 5
                }
                {
                    c'4
                    - \tweak color #blue
                    - \tweak parent-alignment-X #center
                    \sustainOn
                    d'4
                    e'4
                    - \tweak color #red
                    - \tweak parent-alignment-X #center
                    \sustainOff
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> start_piano_pedal = abjad.StartPianoPedal()
            >>> abjad.tweak(start_piano_pedal).color = "#blue"
            >>> abjad.tweak(start_piano_pedal).parent_alignment_X = abjad.Center
            >>> abjad.attach(start_piano_pedal, staff[0])
            >>> stop_piano_pedal = abjad.StopPianoPedal(leak=True)
            >>> abjad.tweak(stop_piano_pedal).color = "#red"
            >>> abjad.tweak(stop_piano_pedal).parent_alignment_X = abjad.Center
            >>> abjad.attach(stop_piano_pedal, staff[-2])
            >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override SustainPedalLineSpanner.staff-padding = 5
                }
                {
                    c'4
                    - \tweak color #blue
                    - \tweak parent-alignment-X #center
                    \sustainOn
                    d'4
                    e'4
                    <>
                    - \tweak color #red
                    - \tweak parent-alignment-X #center
                    \sustainOff
                    r4
                }

        """
        return self._leak

    @property
    def parameter(self) -> str:
        """
        Returns ``'PEDAL'``.

        ..  container:: example

            >>> abjad.StopPianoPedal().parameter
            'PEDAL'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopPianoPedal().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_stop(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopPianoPedal().spanner_stop
            True

        """
        return True

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            REGRESSION. Tweaks survive copy:

            >>> import copy
            >>> stop_piano_pedal = abjad.StopPianoPedal()
            >>> abjad.tweak(stop_piano_pedal).color = "#blue"
            >>> string = abjad.storage(stop_piano_pedal)
            >>> print(string)
            abjad.StopPianoPedal(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

            >>> stop_piano_pedal_2 = copy.copy(stop_piano_pedal)
            >>> string = abjad.storage(stop_piano_pedal_2)
            >>> print(string)
            abjad.StopPianoPedal(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

        """
        return self._tweaks
