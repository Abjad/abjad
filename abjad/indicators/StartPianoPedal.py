import typing

from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..storage import StorageFormatManager


class StartPianoPedal:
    r"""
    LilyPond ``\sustainOn``, ``\sostenutoOn``, ``\unaCorda`` commands.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' r")
        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#blue"
        >>> abjad.tweak(start_piano_pedal).parent_alignment_X = abjad.Center
        >>> abjad.attach(start_piano_pedal, staff[0])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.attach(stop_piano_pedal, staff[1])

        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#red"
        >>> abjad.attach(start_piano_pedal, staff[1])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.attach(stop_piano_pedal, staff[2])

        >>> start_piano_pedal = abjad.StartPianoPedal()
        >>> abjad.tweak(start_piano_pedal).color = "#green"
        >>> abjad.attach(start_piano_pedal, staff[2])
        >>> stop_piano_pedal = abjad.StopPianoPedal()
        >>> abjad.attach(stop_piano_pedal, staff[3])

        >>> abjad.override(staff).SustainPedalLineSpanner.staff_padding = 5
        >>> abjad.setting(staff).pedalSustainStyle = "#'mixed"
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override SustainPedalLineSpanner.staff-padding = 5
                pedalSustainStyle = #'mixed
            }
            {
                c'4
                - \tweak color #blue
                - \tweak parent-alignment-X #center
                \sustainOn
                d'4
                \sustainOff
                - \tweak color #red
                \sustainOn
                e'4
                \sustainOff
                - \tweak color #green
                \sustainOn
                r4
                \sustainOff
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_kind", "_tweaks")

    _context = "StaffGroup"

    _persistent = True

    _parameter = "PEDAL"

    ### INITIALIZER ###

    def __init__(self, kind: str = None, *, tweaks: TweakInterface = None) -> None:
        if kind is not None:
            assert kind in ("sustain", "sostenuto", "corda")
        self._kind = kind
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        if self.kind == "corda":
            string = r"\unaCorda"
        elif self.kind == "sostenuto":
            string = r"\sostenutoOn"
        else:
            assert self.kind in ("sustain", None)
            string = r"\sustainOn"
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'StaffGroup'``.

        ..  container:: example

            >>> abjad.StartPianoPedal().context
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
    def parameter(self) -> str:
        """
        Returns ``'PEDAL'``.

        ..  container:: example

            >>> abjad.StartPianoPedal().parameter
            'PEDAL'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartPianoPedal().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_start(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartPianoPedal().spanner_start
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
            >>> start_piano_pedal = abjad.StartPianoPedal()
            >>> abjad.tweak(start_piano_pedal).color = "#blue"
            >>> string = abjad.storage(start_piano_pedal)
            >>> print(string)
            abjad.StartPianoPedal(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

            >>> start_piano_pedal_2 = copy.copy(start_piano_pedal)
            >>> string = abjad.storage(start_piano_pedal_2)
            >>> print(string)
            abjad.StartPianoPedal(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

        """
        return self._tweaks
