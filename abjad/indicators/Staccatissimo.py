import typing
from abjad import enums
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.utilities.String import String


class Staccatissimo(AbjadValueObject):
    r"""
    Staccatissimo.

    ..  container:: example

        Attached to a single note:

        >>> note = abjad.Note("c'4")
        >>> staccatissimo = abjad.Staccatissimo()
        >>> abjad.attach(staccatissimo, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4
            \staccatissimo

    ..  container:: example

        Attached to notes in a staff:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> abjad.attach(abjad.Beam(), staff[:4])
        >>> abjad.attach(abjad.Beam(), staff[4:])
        >>> abjad.attach(abjad.Staccatissimo(), staff[3])
        >>> abjad.attach(abjad.Staccatissimo(), staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                [
                d'8
                e'8
                f'8
                ]
                \staccatissimo
                g'8
                [
                a'8
                b'8
                c''8
                ]
                \staccatissimo
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_tweaks',
        )

    _format_slot: enums.HorizontalAlignment = enums.Right

    _time_orientation: enums.HorizontalAlignment = enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: enums.VerticalAlignment = None,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        direction_ = String.to_tridirectional_ordinal_constant(direction)
        if direction_ is not None:
            assert isinstance(direction_, enums.VerticalAlignment), repr(direction_)
            directions = (enums.Up, enums.Down, enums.Center, None)
            assert direction_ in directions, repr(direction_)
        self._direction = direction_
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""Gets string representation of staccatissimo.

        ..  container:: example

            >>> str(abjad.Staccatissimo())
            '\\staccatissimo'

        """
        return r'\staccatissimo'

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.commands.extend(tweaks)
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[enums.VerticalAlignment]:
        """
        Gets direction of articulation.

        ..  container:: example

            Without direction:

            >>> abjad.Staccatissimo().direction is None
            True

            >>> abjad.Staccatissimo(direction=abjad.Up).direction
            Up

        """
        return self._direction


    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> staccatissimo = abjad.Staccatissimo()
            >>> abjad.tweak(staccatissimo).color = 'blue'
            >>> abjad.attach(staccatissimo, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                \staccatissimo

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> staccatissimo = abjad.Staccatissimo(tweaks=[('color', 'blue')])
            >>> abjad.attach(staccatissimo, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                \staccatissimo

        """
        return self._tweaks
