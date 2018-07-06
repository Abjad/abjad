import typing
from abjad import enums
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class LaissezVibrer(AbjadValueObject):
    r"""
    Laissez vibrer.

    ..  container:: example

        >>> chord = abjad.Chord("<c' e' g' c''>4")
        >>> laissez_vibrer = abjad.LaissezVibrer()
        >>> abjad.attach(laissez_vibrer, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <c' e' g' c''>4
            \laissezVibrer

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_tweaks',
        )

    _format_slot = 'after'

    _time_orientation: enums.HorizontalAlignment = enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""
        Gets string representation of laissez vibrer indicator.

        ..  container:: example

            Default:

            >>> str(abjad.LaissezVibrer())
            '\\laissezVibrer'

        """
        return r'\laissezVibrer'

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
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> lv = abjad.LaissezVibrer()
            >>> abjad.tweak(lv).color = 'blue'
            >>> abjad.attach(lv, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                \laissezVibrer

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> lv = abjad.LaissezVibrer(tweaks=[('color', 'blue')])
            >>> abjad.attach(lv, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                \laissezVibrer

        """
        return self._tweaks
