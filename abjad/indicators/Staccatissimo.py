import typing

from abjad import enums
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.String import String


class Staccatissimo(object):
    r"""
    Staccatissimo.

    ..  container:: example

        >>> staff = abjad.Staff("c'4")
        >>> abjad.attach(abjad.Staccatissimo(), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \staccatissimo
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_direction", "_tweaks")

    _format_slot = enums.Right

    _time_orientation = enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: enums.VerticalAlignment = None,
        tweaks: LilyPondTweakManager = None,
    ) -> None:
        direction_ = String.to_tridirectional_ordinal_constant(direction)
        if direction_ is not None:
            assert isinstance(direction_, enums.VerticalAlignment), repr(direction_)
            directions = (enums.Up, enums.Down, enums.Center, None)
            assert direction_ in directions, repr(direction_)
        self._direction = direction_
        if tweaks is not None:
            assert isinstance(tweaks, LilyPondTweakManager), repr(tweaks)
        self._tweaks = LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to storage format manager.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Delegates to storage format manager.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Delegates to storage format manager.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        r"""
        Gets string representation of staccatissimo.

        ..  container:: example

            >>> str(abjad.Staccatissimo())
            '\\staccatissimo'

        """
        string = r"\staccatissimo"
        if self.direction is None:
            return string
        direction = String.to_tridirectional_lilypond_symbol(self.direction)
        assert isinstance(direction, String), repr(direction)
        return fr"{direction} {string}"

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
        r"""
        Gets direction of staccatissimo.

        ..  container:: example

            With ``direction`` unset:

            >>> staff = abjad.Staff("c'4 c''4")
            >>> abjad.attach(abjad.Staccatissimo(), staff[0])
            >>> abjad.attach(abjad.Staccatissimo(), staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \staccatissimo
                    c''4
                    \staccatissimo
                }

            With ``direction=abjad.Up``:

            >>> staff = abjad.Staff("c'4 c''4")
            >>> abjad.attach(abjad.Staccatissimo(direction=abjad.Up), staff[0])
            >>> abjad.attach(abjad.Staccatissimo(direction=abjad.Up), staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    ^ \staccatissimo
                    c''4
                    ^ \staccatissimo
                }

            With ``direction=abjad.Down``:

            >>> staff = abjad.Staff("c'4 c''4")
            >>> abjad.attach(abjad.Staccatissimo(direction=abjad.Down), staff[0])
            >>> abjad.attach(abjad.Staccatissimo(direction=abjad.Down), staff[1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    _ \staccatissimo
                    c''4
                    _ \staccatissimo
                }

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

        """
        return self._tweaks
