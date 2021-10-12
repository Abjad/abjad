import typing

from .. import enums
from .. import format as _format
from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..string import String


class StartSlur:
    r"""
    LilyPond ``(`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_slur = abjad.StartSlur()
        >>> abjad.tweak(start_slur).color = "#blue"
        >>> abjad.attach(start_slur, staff[0])
        >>> stop_slur = abjad.StopSlur()
        >>> abjad.attach(stop_slur, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                (
                d'4
                e'4
                f'4
                )
            }

    ..  container:: example

        >>> abjad.StartSlur()
        StartSlur()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_direction", "_tweaks")

    _context = "Voice"

    _parameter = "SLUR"

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: enums.VerticalAlignment = None,
        tweaks: TweakInterface = None,
    ) -> None:
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
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
        Hashes start slur.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _add_direction(self, string):
        if getattr(self, "direction", None) is not None:
            string = f"{self.direction} {string}"
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction("(")
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StartSlur().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def direction(self) -> typing.Optional[str]:
        r"""
        Gets direction.

        ..  container:: example

            With ``direction`` unset:

            >>> staff = abjad.Staff("c'8 d' e' f' c'' d'' e'' f''")
            >>> abjad.attach(abjad.StartSlur(), staff[0])
            >>> abjad.attach(abjad.StopSlur(), staff[3])
            >>> abjad.attach(abjad.StartSlur(), staff[4])
            >>> abjad.attach(abjad.StopSlur(), staff[7])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'8
                    (
                    d'8
                    e'8
                    f'8
                    )
                    c''8
                    (
                    d''8
                    e''8
                    f''8
                    )
                }

            With ``direction=abjad.Up``:

            >>> staff = abjad.Staff("c'8 d' e' f' c'' d'' e'' f''")
            >>> abjad.attach(abjad.StartSlur(direction=abjad.Up), staff[0])
            >>> abjad.attach(abjad.StopSlur(), staff[3])
            >>> abjad.attach(abjad.StartSlur(direction=abjad.Up), staff[4])
            >>> abjad.attach(abjad.StopSlur(), staff[7])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'8
                    ^ (
                    d'8
                    e'8
                    f'8
                    )
                    c''8
                    ^ (
                    d''8
                    e''8
                    f''8
                    )
                }

            With ``direction=abjad.Down``:

            >>> staff = abjad.Staff("c'8 d' e' f' c'' d'' e'' f''")
            >>> abjad.attach(abjad.StartSlur(direction=abjad.Down), staff[0])
            >>> abjad.attach(abjad.StopSlur(), staff[3])
            >>> abjad.attach(abjad.StartSlur(direction=abjad.Down), staff[4])
            >>> abjad.attach(abjad.StopSlur(), staff[7])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'8
                    _ (
                    d'8
                    e'8
                    f'8
                    )
                    c''8
                    _ (
                    d''8
                    e''8
                    f''8
                    )
                }

        """
        return self._direction

    @property
    def parameter(self) -> str:
        """
        Returns ``'SLUR'``.

        ..  container:: example

            >>> abjad.StartSlur().parameter
            'SLUR'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartSlur().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_start(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartSlur().spanner_start
            True

        """
        return True

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            REGRESSION. Tweaks survive copy:

            >>> import copy
            >>> start_slur = abjad.StartSlur()
            >>> abjad.tweak(start_slur).color = "#blue"
            >>> string = abjad.storage(start_slur)
            >>> print(string)
            abjad.StartSlur(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

            >>> start_slur_2 = copy.copy(start_slur)
            >>> string = abjad.storage(start_slur_2)
            >>> print(string)
            abjad.StartSlur(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

        """
        return self._tweaks
