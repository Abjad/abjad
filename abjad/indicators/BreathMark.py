import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.enumerations import HorizontalAlignment
from abjad.enumerations import Right
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class BreathMark(AbjadValueObject):
    r"""
    Breath mark.

    ..  container:: example

        Attached to a single note:

        >>> note = abjad.Note("c'4")
        >>> breath_mark = abjad.BreathMark()
        >>> abjad.attach(breath_mark, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4
            \breathe

    ..  container:: example

        Attached to notes in a staff:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> abjad.attach(abjad.Beam(), staff[:4])
        >>> abjad.attach(abjad.Beam(), staff[4:])
        >>> abjad.attach(abjad.BreathMark(), staff[3])
        >>> abjad.attach(abjad.BreathMark(), staff[7])
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
                \breathe
                g'8
                [
                a'8
                b'8
                c''8
                ]
                \breathe
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lilypond_tweak_manager',
        )

    _format_slot = 'after'

    _time_orientation: HorizontalAlignment = HorizontalAlignment.Right

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        self._lilypond_tweak_manager = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r"""
        Gets string representation of breath mark.

        ..  container:: example

            >>> str(abjad.BreathMark())
            '\\breathe'

        """
        return r'\breathe'

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
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.right.articulations.extend(tweaks)
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> breath = abjad.BreathMark()
            >>> abjad.tweak(breath).color = 'blue'
            >>> abjad.attach(breath, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                \tweak color #blue
                \breathe

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> breath = abjad.BreathMark(tweaks=[('color', 'blue')])
            >>> abjad.attach(breath, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                \tweak color #blue
                \breathe

        """
        return self._lilypond_tweak_manager
