import dataclasses
import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import overrides as _overrides
from .. import string as _string


@dataclasses.dataclass
class Arpeggio:
    r"""
    Arpeggio.

    ..  container:: example

        Without direction arrow:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio()
        >>> abjad.attach(arpeggio, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' e' g' c''>4
                \arpeggio
            }

    ..  container:: example

        With direction arrow:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio(direction=abjad.Down)
        >>> abjad.attach(arpeggio, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \arpeggioArrowDown
                <c' e' g' c''>4
                \arpeggio
            }

    ..  container:: example

        Tweaks:

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> arpeggio = abjad.Arpeggio()
        >>> abjad.tweak(arpeggio).color = "#blue"
        >>> abjad.attach(arpeggio, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' e' g' c''>4
                - \tweak color #blue
                \arpeggio
            }

    """

    direction: typing.Union[int, _enums.VerticalAlignment, None] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    def __post_init__(self):
        self._annotation = None
        self.direction = _string.String.to_tridirectional_ordinal_constant(
            self.direction
        )
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format(self):
        return r"\arpeggio"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(r"\arpeggio")
        if self.direction in (_enums.Up, _enums.Down):
            if self.direction is _enums.Up:
                command = r"\arpeggioArrowUp"
            else:
                command = r"\arpeggioArrowDown"
            bundle.before.commands.append(command)
        return bundle
