import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import format as _format
from .. import overrides as _overrides


class StartPhrasingSlur:
    r"""
    LilyPond ``(`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_phrasing_slur = abjad.StartPhrasingSlur()
        >>> abjad.tweak(start_phrasing_slur).color = "#blue"
        >>> abjad.attach(start_phrasing_slur, staff[0])
        >>> stop_phrasing_slur = abjad.StopPhrasingSlur()
        >>> abjad.attach(stop_phrasing_slur, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \(
                d'4
                e'4
                f'4
                \)
            }

    ..  container:: example

        >>> abjad.StartPhrasingSlur()
        StartPhrasingSlur()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_direction", "_tweaks")

    context = "Voice"
    parameter = "PHRASING_SLUR"
    persistent = True
    spanner_start = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: _enums.VerticalAlignment = None,
        tweaks: _overrides.TweakInterface = None,
    ) -> None:
        self._direction = direction
        if tweaks is not None:
            assert isinstance(tweaks, _overrides.TweakInterface), repr(tweaks)
        self._tweaks = _overrides.TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes start phrasing slur.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _add_direction(self, string):
        if getattr(self, "direction", False):
            string = f"{self.direction} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction(r"\(")
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[_enums.VerticalAlignment]:
        """
        Gets direction.
        """
        return self._direction

    @property
    def tweaks(self) -> typing.Optional[_overrides.TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            REGRESSION. Tweaks survive copy:

            >>> import copy
            >>> start_phrasing_slur = abjad.StartPhrasingSlur()
            >>> abjad.tweak(start_phrasing_slur).color = "#blue"
            >>> string = abjad.storage(start_phrasing_slur)
            >>> print(string)
            abjad.StartPhrasingSlur(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

            >>> start_phrasing_slur_2 = copy.copy(start_phrasing_slur)
            >>> string = abjad.storage(start_phrasing_slur_2)
            >>> print(string)
            abjad.StartPhrasingSlur(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

        """
        return self._tweaks
