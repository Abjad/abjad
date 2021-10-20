import dataclasses
import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import overrides as _overrides


@dataclasses.dataclass(unsafe_hash=True)
class LaissezVibrer:
    r"""
    Laissez vibrer.

    ..  container:: example

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> laissez_vibrer = abjad.LaissezVibrer()
        >>> abjad.attach(laissez_vibrer, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(chord)
            >>> print(string)
            <c' e' g' c''>4
            \laissezVibrer

    ..  container:: example

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> lv = abjad.LaissezVibrer()
        >>> abjad.tweak(lv).color = "#blue"
        >>> abjad.attach(lv, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            \laissezVibrer

    """

    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    _format_slot = "after"

    _time_orientation = _enums.Right

    def __str__(self) -> str:
        r"""
        Gets string representation of laissez vibrer indicator.

        ..  container:: example

            Default:

            >>> str(abjad.LaissezVibrer())
            '\\laissezVibrer'

        """
        return r"\laissezVibrer"

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle
