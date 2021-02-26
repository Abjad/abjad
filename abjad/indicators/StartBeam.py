import typing

from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..storage import StorageFormatManager
from ..string import String


class StartBeam:
    r"""
    LilyPond ``[`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d' e' f'")
        >>> start_beam = abjad.StartBeam()
        >>> abjad.tweak(start_beam).color = "#blue"
        >>> abjad.attach(start_beam, staff[0])
        >>> stop_beam = abjad.StopBeam()
        >>> abjad.attach(stop_beam, staff[-1])
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
                f'8
                ]
            }

    ..  container:: example

        >>> abjad.StartBeam()
        StartBeam()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_direction", "_tweaks")

    _context = "Voice"

    _parameter = "BEAM"

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, *, direction: int = None, tweaks: TweakInterface = None) -> None:
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
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
        if getattr(self, "direction", None) is not None:
            string = f"{self.direction} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction("[")
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StartBeam().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def direction(self) -> typing.Optional[str]:
        """
        Gets direction.
        """
        return self._direction

    @property
    def parameter(self) -> str:
        """
        Returns ``'BEAM'``.

        ..  container:: example

            >>> abjad.StartBeam().parameter
            'BEAM'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartBeam().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_start(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartBeam().spanner_start
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
            >>> start_beam = abjad.StartBeam()
            >>> abjad.tweak(start_beam).color = "#blue"
            >>> string = abjad.storage(start_beam)
            >>> print(string)
            abjad.StartBeam(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

            >>> start_beam_2 = copy.copy(start_beam)
            >>> string = abjad.storage(start_beam_2)
            >>> print(string)
            abjad.StartBeam(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

        """
        return self._tweaks
