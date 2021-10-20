import dataclasses
import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import overrides as _overrides
from .. import typings as _typings


@dataclasses.dataclass
class BendAfter:
    r"""
    Fall or doit.

    ..  container:: example

        A fall:

        >>> note = abjad.Note("c'4")
        >>> bend = abjad.BendAfter(-4)
        >>> abjad.attach(bend, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \bendAfter #'-4

    ..  container:: example

        A doit:

        >>> note = abjad.Note("c'4")
        >>> bend = abjad.BendAfter(2)
        >>> abjad.attach(bend, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \bendAfter #'2

    ..  container:: example

        Tweaks:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> bend_after = abjad.BendAfter(-4)
        >>> abjad.tweak(bend_after).color = "#blue"
        >>> abjad.attach(bend_after, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                - \bendAfter #'-4
                d'4
                e'4
                f'4
            }

    """

    bend_amount: _typings.Number = -4
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _format_slot = "after"
    _is_dataclass = True
    _time_orientation = _enums.Right

    # TODO: remove
    def __str__(self) -> str:
        r"""
        Gets string representation of bend after.

        ..  container:: example

            >>> str(abjad.BendAfter())
            "- \\bendAfter #'-4"

        """
        return rf"- \bendAfter #'{self.bend_amount}"

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle
