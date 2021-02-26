import typing

from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..storage import StorageFormatManager


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

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, *, tweaks: TweakInterface = None) -> None:
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

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

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = r"\startGroup"
        bundle.after.spanner_starts.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartGroup().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_start(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartGroup().spanner_start
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
