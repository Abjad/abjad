import typing

from abjad import enums
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tags import Tags
from abjad.top.inspect import inspect
from abjad.utilities.Duration import Duration
from abjad.utilities.String import String

from .Clef import Clef

abjad_tags = Tags()


class RepeatTie(object):
    r"""
    LilyPond ``\repeatTie`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c' d' d'")
        >>> repeat_tie = abjad.RepeatTie()
        >>> abjad.tweak(repeat_tie).color = 'blue'
        >>> abjad.attach(repeat_tie, staff[1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                c'4
                - \tweak color #blue
                \repeatTie
                d'4
                d'4
            }

        >>> for leaf in staff:
        ...     leaf, abjad.inspect(leaf).logical_tie()
        ...
        (Note("c'4"), LogicalTie([Note("c'4"), Note("c'4")]))
        (Note("c'4"), LogicalTie([Note("c'4"), Note("c'4")]))
        (Note("d'4"), LogicalTie([Note("d'4")]))
        (Note("d'4"), LogicalTie([Note("d'4")]))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_direction", "_tweaks")

    _context = "Voice"

    _persistent = True

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: enums.VerticalAlignment = None,
        tweaks: LilyPondTweakManager = None,
    ) -> None:
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
        if tweaks is not None:
            assert isinstance(tweaks, LilyPondTweakManager), repr(tweaks)
        self._tweaks = LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        from abjad.core.Chord import Chord
        from abjad.core.Note import Note

        if not isinstance(argument, (Chord, Note)):
            string = f"Must be note or chord (not {argument})."
            return [string]
        previous_leaf = inspect(argument).leaf(-1)
        if not isinstance(previous_leaf, (Chord, Note, type(None))):
            string = f"Can not attach repeat-tie to {argument}"
            string += f" when previous leaf is {previous_leaf}."
            return [string]
        return True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            strings = self.tweaks._list_format_contributions()
            bundle.after.spanners.extend(strings)
        strings = []
        if self.direction is not None:
            assert isinstance(self.direction, str)
            strings.append(self.direction)
        elif self._should_force_repeat_tie_up(component):
            string = r"- \tweak direction #up"
            strings.append(string)
        strings.append(r"\repeatTie")
        bundle.after.spanners.extend(strings)
        return bundle

    @staticmethod
    def _should_force_repeat_tie_up(leaf):
        from abjad.core.Chord import Chord
        from abjad.core.Note import Note

        if not isinstance(leaf, (Note, Chord)):
            return False
        if leaf.written_duration < Duration(1):
            return False
        clef = inspect(leaf).effective(Clef, default=Clef("treble"))
        if isinstance(leaf, Note):
            written_pitches = [leaf.written_pitch]
        else:
            written_pitches = leaf.written_pitches
        for written_pitch in written_pitches:
            staff_position = written_pitch.to_staff_position(clef=clef)
            if staff_position.number == 0:
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.RepeatTie().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def direction(self) -> typing.Optional[String]:
        r"""
        Gets direction.

        ..  container:: example

            With ``direction`` unset:

            >>> staff = abjad.Staff("c'4 c'4 c''4 c''4")
            >>> tie = abjad.RepeatTie()
            >>> abjad.tweak(tie).color = 'blue'
            >>> abjad.attach(tie, staff[1])
            >>> tie = abjad.RepeatTie()
            >>> abjad.tweak(tie).color = 'blue'
            >>> abjad.attach(tie, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    c'4
                    - \tweak color #blue
                    \repeatTie
                    c''4
                    c''4
                    - \tweak color #blue
                    \repeatTie
                }

            With ``direction=abjad.Up``:

            >>> staff = abjad.Staff("c'4 c'4 c''4 c''4")
            >>> tie = abjad.RepeatTie(direction=abjad.Up)
            >>> abjad.tweak(tie).color = 'blue'
            >>> abjad.attach(tie, staff[1])
            >>> tie = abjad.RepeatTie(direction=abjad.Up)
            >>> abjad.tweak(tie).color = 'blue'
            >>> abjad.attach(tie, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    c'4
                    - \tweak color #blue
                    ^
                    \repeatTie
                    c''4
                    c''4
                    - \tweak color #blue
                    ^
                    \repeatTie
                }

            With ``direction=abjad.Down``:

            >>> staff = abjad.Staff("c'4 c'4 c''4 c''4")
            >>> tie = abjad.RepeatTie(direction=abjad.Down)
            >>> abjad.tweak(tie).color = 'blue'
            >>> abjad.attach(tie, staff[1])
            >>> tie = abjad.RepeatTie(direction=abjad.Down)
            >>> abjad.tweak(tie).color = 'blue'
            >>> abjad.attach(tie, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    c'4
                    - \tweak color #blue
                    _
                    \repeatTie
                    c''4
                    c''4
                    - \tweak color #blue
                    _
                    \repeatTie
                }

        """
        return self._direction

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.RepeatTie().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> staff = abjad.Staff("c'4 c' d' d'")
            >>> repeat_tie = abjad.RepeatTie()
            >>> abjad.tweak(repeat_tie).color = 'blue'
            >>> abjad.attach(repeat_tie, staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    c'4
                    - \tweak color #blue
                    \repeatTie
                    d'4
                    d'4
                }

        """
        return self._tweaks
