import typing
from abjad import enums
from abjad import typings
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class BendAfter(AbjadValueObject):
    r"""
    Fall or doit.

    ..  container:: example

        A fall:

        >>> note = abjad.Note("c'4")
        >>> bend = abjad.BendAfter(-4)
        >>> abjad.attach(bend, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4
            - \bendAfter #'-4

    ..  container:: example

        A doit:

        >>> note = abjad.Note("c'4")
        >>> bend = abjad.BendAfter(2)
        >>> abjad.attach(bend, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4
            - \bendAfter #'2

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bend_amount',
        '_tweaks',
        )

    _format_slot = 'after'

    _time_orientation: enums.HorizontalAlignment = enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        bend_amount: typings.Number = -4,
        *,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        assert isinstance(bend_amount, (int, float)), repr(bend_amount)
        self._bend_amount = bend_amount
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""
        Gets string representation of bend after.

        ..  container:: example

            >>> str(abjad.BendAfter())
            "- \\bendAfter #'-4"

        """
        return rf"- \bendAfter #'{self.bend_amount}"

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def bend_amount(self) -> typings.Number:
        """
        Gets bend amount of bend after.

        ..  container:: example

            Fall:

            >>> bend = abjad.BendAfter(-4)
            >>> bend.bend_amount
            -4

        ..  container:: example

            Doit:

            >>> bend = abjad.BendAfter(2.5)
            >>> bend.bend_amount
            2.5

        """
        return self._bend_amount

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> bend = abjad.BendAfter(-4, tweaks=[('color', 'blue')])
            >>> abjad.attach(bend, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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
        return self._tweaks
