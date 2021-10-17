import dataclasses
import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import overrides as _overrides


@dataclasses.dataclass
class BreathMark:
    r"""
    Breath mark.

    ..  container:: example

        Attached to a single note:

        >>> note = abjad.Note("c'4")
        >>> breath_mark = abjad.BreathMark()
        >>> abjad.attach(breath_mark, note)
        >>> staff = abjad.Staff([note])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \breathe
            }

    ..  container:: example

        Attached to notes in a staff:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> abjad.beam(staff[:4])
        >>> abjad.beam(staff[4:])
        >>> abjad.attach(abjad.BreathMark(), staff[3])
        >>> abjad.attach(abjad.BreathMark(), staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                [
                d'8
                e'8
                f'8
                ]
                \breathe
                g'8
                [
                a'8
                b'8
                c''8
                ]
                \breathe
            }

    ..  container:: example

        REGRESSION. Abjad parses LilyPond's ``\breathe`` command correctly:

        >>> staff = abjad.Staff(r"c'4 d' e' f' \breathe")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \breathe
            }

    ..  container:: example

        Works with tweaks:

        >>> note = abjad.Note("c'4")
        >>> breath = abjad.BreathMark()
        >>> abjad.tweak(breath).color = "#blue"
        >>> abjad.attach(breath, note)
        >>> staff = abjad.Staff([note])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                \tweak color #blue
                \breathe
            }

    """

    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _format_slot = "after"

    _is_dataclass = True

    _time_orientation = _enums.Right

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format(self):
        return r"\breathe"

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.after.articulations.extend(tweaks)
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle
