import typing
from abjad.enumerations import (
    Center, Down, Right, Up, HorizontalAlignment, VerticalAlignment,
)
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.String import String
from abjad.tools.lilypondnametools.LilyPondTweakManager import (
    LilyPondTweakManager,
    )
from abjad.tools.systemtools.LilyPondFormatBundle import LilyPondFormatBundle


class Staccato(AbjadValueObject):
    r"""
    Staccato.

    ..  container:: example

        Attached to a single note:

        >>> note = abjad.Note("c'4")
        >>> staccato = abjad.Staccato()
        >>> abjad.attach(staccato, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4
            \staccato

    ..  container:: example

        Attached to notes in a staff:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> abjad.attach(abjad.Beam(), staff[:4])
        >>> abjad.attach(abjad.Beam(), staff[4:])
        >>> abjad.attach(abjad.Staccato(), staff[3])
        >>> abjad.attach(abjad.Staccato(), staff[7])
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
                \staccato
                g'8
                [
                a'8
                b'8
                c''8
                ]
                \staccato
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_lilypond_tweak_manager',
        )

    _format_slot: HorizontalAlignment = HorizontalAlignment.Right

    _time_orientation: HorizontalAlignment = HorizontalAlignment.Right

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: VerticalAlignment = None,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        direction_ = String.to_tridirectional_ordinal_constant(direction)
        if direction_ is not None:
            assert isinstance(direction_, VerticalAlignment), repr(direction_)
            directions = (Up, Down, Center, None)
            assert direction_ in directions, repr(direction_)
        self._direction = direction_
        self._lilypond_tweak_manager = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""
        Gets string representation of staccato.

        ..  container:: example

            >>> str(abjad.Staccato())
            '\\staccato'

        """
        return r'\staccato'

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

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
    def direction(self) -> typing.Optional[VerticalAlignment]:
        """
        Gets direction of articulation.

        ..  container:: example

            Without direction:

            >>> abjad.Staccato().direction is None
            True

            >>> abjad.Staccato(direction=abjad.Up).direction
            Up

        """
        return self._direction

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> staccato = abjad.Staccato()
            >>> abjad.tweak(staccato).color = 'blue'
            >>> abjad.attach(staccato, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                \staccato

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> staccato = abjad.Staccato(tweaks=[('color', 'blue')])
            >>> abjad.attach(staccato, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                - \tweak color #blue
                \staccato

        """
        return self._lilypond_tweak_manager
