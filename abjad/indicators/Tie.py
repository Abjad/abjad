import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import format as _format
from .. import overrides as _overrides
from .. import string as _string


class Tie:
    r"""
    LilyPond ``~`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c' d' d'")
        >>> tie = abjad.Tie()
        >>> abjad.tweak(tie).color = "#blue"
        >>> abjad.attach(tie, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                ~
                c'4
                d'4
                d'4
            }

        >>> for leaf in staff:
        ...     leaf, abjad.get.logical_tie(leaf)
        ...
        (Note("c'4"), LogicalTie([Note("c'4"), Note("c'4")]))
        (Note("c'4"), LogicalTie([Note("c'4"), Note("c'4")]))
        (Note("d'4"), LogicalTie([Note("d'4")]))
        (Note("d'4"), LogicalTie([Note("d'4")]))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_direction", "_tweaks")

    context = "Voice"
    persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: _enums.VerticalAlignment = None,
        tweaks: _overrides.TweakInterface = None,
    ) -> None:
        direction_ = _string.String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
        if tweaks is not None:
            assert isinstance(tweaks, _overrides.TweakInterface), repr(tweaks)
        self._tweaks = _overrides.TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes tie.
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

    def _attachment_test_all(self, argument):
        if not (
            hasattr(argument, "written_pitch") or hasattr(argument, "written_pitches")
        ):
            string = f"Must be note or chord (not {argument})."
            return [string]
        return True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            strings = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(strings)
        string = self._add_direction("~")
        strings = [string]
        bundle.after.spanner_starts.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> typing.Optional[str]:
        r"""
        Gets direction.

        ..  container:: example

            With ``direction`` unset:

            >>> staff = abjad.Staff("c'4 c' c'' c''")
            >>> abjad.attach(abjad.Tie(), staff[0])
            >>> abjad.attach(abjad.Tie(), staff[2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    ~
                    c'4
                    c''4
                    ~
                    c''4
                }

            With ``direction=abjad.Up``:

            >>> staff = abjad.Staff("c'4 c' c'' c''")
            >>> abjad.attach(abjad.Tie(direction=abjad.Up), staff[0])
            >>> abjad.attach(abjad.Tie(direction=abjad.Up), staff[2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    ^ ~
                    c'4
                    c''4
                    ^ ~
                    c''4
                }

            With ``direction=abjad.Down``:

            >>> staff = abjad.Staff("c'4 c' c'' c''")
            >>> abjad.attach(abjad.Tie(direction=abjad.Down), staff[0])
            >>> abjad.attach(abjad.Tie(direction=abjad.Down), staff[2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    _ ~
                    c'4
                    c''4
                    _ ~
                    c''4
                }

        """
        return self._direction

    @property
    def tweaks(self) -> typing.Optional[_overrides.TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> staff = abjad.Staff("c'4 c' d' d'")
            >>> tie = abjad.Tie()
            >>> abjad.tweak(tie).color = "#blue"
            >>> abjad.attach(tie, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    ~
                    c'4
                    d'4
                    d'4
                }

        """
        return self._tweaks
