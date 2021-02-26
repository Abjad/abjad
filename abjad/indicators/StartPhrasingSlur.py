import typing

from .. import enums
from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..storage import StorageFormatManager


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

    _context = "Voice"

    _parameter = "PHRASING_SLUR"

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: enums.VerticalAlignment = None,
        tweaks: TweakInterface = None,
    ) -> None:
        self._direction = direction
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

    def _add_direction(self, string):
        if getattr(self, "direction", False):
            string = f"{self.direction} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction(r"\(")
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StartPhrasingSlur().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def direction(self) -> typing.Optional[enums.VerticalAlignment]:
        """
        Gets direction.
        """
        return self._direction

    @property
    def parameter(self) -> str:
        """
        Returns ``'PHRASING_SLUR'``.

        ..  container:: example

            >>> abjad.StartPhrasingSlur().parameter
            'PHRASING_SLUR'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartPhrasingSlur().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_start(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartPhrasingSlur().spanner_start
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
