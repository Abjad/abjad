import typing

from .. import bundle as _bundle
from .. import format as _format
from .. import overrides as _overrides


class StartGroup:
    r"""
    LilyPond ``\startGroup`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_group = abjad.StartGroup()
        >>> abjad.tweak(start_group).color = "#blue"
        >>> abjad.attach(start_group, staff[0])
        >>> stop_group = abjad.StopGroup()
        >>> abjad.attach(stop_group, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \startGroup
                d'4
                e'4
                f'4
                \stopGroup
            }

    ..  container:: example

        >>> abjad.StartGroup()
        StartGroup()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_tweaks",)

    persistent = True
    spanner_start = True

    ### INITIALIZER ###

    def __init__(self, *, tweaks: _overrides.TweakInterface = None) -> None:
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
        Hashes start group.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = r"\startGroup"
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def tweaks(self) -> typing.Optional[_overrides.TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            REGRESSION. Tweaks survive copy:

            >>> import copy
            >>> start_group = abjad.StartGroup()
            >>> abjad.tweak(start_group).color = "#blue"
            >>> string = abjad.storage(start_group)
            >>> print(string)
            abjad.StartGroup(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

            >>> start_group_2 = copy.copy(start_group)
            >>> string = abjad.storage(start_group_2)
            >>> print(string)
            abjad.StartGroup(
                tweaks=TweakInterface(('_literal', None), ('color', '#blue')),
                )

        """
        return self._tweaks
