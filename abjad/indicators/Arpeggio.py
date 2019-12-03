import typing

from abjad import enums
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class Arpeggio(object):
    r"""
    Arpeggio.

    ..  container:: example

        Without direction arrow:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio()
        >>> abjad.attach(arpeggio, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <c' e' g' c''>4
            \arpeggio

    ..  container:: example

        With direction arrow:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio(direction=abjad.Down)
        >>> abjad.attach(arpeggio, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            \arpeggioArrowDown
            <c' e' g' c''>4
            \arpeggio

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_direction", "_tweaks")

    ### INITIALIZER ###

    def __init__(
        self, *, direction: int = None, tweaks: LilyPondTweakManager = None
    ) -> None:
        if direction is not None:
            assert direction in (enums.Up, enums.Down, enums.Center)
        self._direction = direction
        if tweaks is not None:
            assert isinstance(tweaks, LilyPondTweakManager), repr(tweaks)
        self._tweaks = LilyPondTweakManager.set_tweaks(self, tweaks)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return r"\arpeggio"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(r"\arpeggio")
        if self.direction in (enums.Up, enums.Down):
            if self.direction is enums.Up:
                command = r"\arpeggioArrowUp"
            else:
                command = r"\arpeggioArrowDown"
            bundle.before.commands.append(command)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[int]:
        """
        Gets direction of arpeggio.

        ..  container:: example

            Without direction arrow:

            >>> arpeggio = abjad.Arpeggio()
            >>> arpeggio.direction is None
            True

        ..  container:: example

            With direction arrow:

            >>> arpeggio = abjad.Arpeggio(direction=abjad.Down)
            >>> arpeggio.direction
            Down

        """
        return self._direction

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> chord = abjad.Chord("<c' e' g' c''>4")
            >>> arpeggio = abjad.Arpeggio()
            >>> abjad.tweak(arpeggio).color = 'blue'
            >>> abjad.attach(arpeggio, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <c' e' g' c''>4
                - \tweak color #blue
                \arpeggio

        """
        return self._tweaks
