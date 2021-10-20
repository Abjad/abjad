import typing

from .. import bundle as _bundle
from .. import format as _format
from .. import overrides as _overrides
from .. import string as _string


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

    context = "Voice"
    parameter = "BEAM"
    persistent = True
    spanner_start = True

    ### INITIALIZER ###

    def __init__(
        self, *, direction: int = None, tweaks: _overrides.TweakInterface = None
    ) -> None:
        direction_ = _string.String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
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
        Hashes start beam.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _add_direction(self, string):
        if getattr(self, "direction", None) is not None:
            string = f"{self.direction} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction("[")
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[str]:
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
