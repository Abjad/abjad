import typing

from .. import enums
from .. import format as _format
from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface


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

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_tweaks",)

    _format_slot = "after"

    _time_orientation = enums.Right

    ### INITIALIZER ###

    def __init__(self, *, tweaks: TweakInterface = None) -> None:
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes laissez vibrer.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self) -> str:
        r"""
        Gets string representation of laissez vibrer indicator.

        ..  container:: example

            Default:

            >>> str(abjad.LaissezVibrer())
            '\\laissezVibrer'

        """
        return r"\laissezVibrer"

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
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

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
        return self._tweaks
