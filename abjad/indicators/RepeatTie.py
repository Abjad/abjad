import typing
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager


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

    __slots__ = (
        '_left_broken',
        '_tweaks',
        )

    _context = 'Voice'

    _persistent = True

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        left_broken: bool = None,
        tweaks: LilyPondTweakManager = None,
        ) -> None:
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        if tweaks is not None:
            assert isinstance(tweaks, LilyPondTweakManager), repr(tweaks)
        LilyPondTweakManager.set_tweaks(self, tweaks)

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
            raise TypeError(f'unhashable type: {self}')
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
            bundle.after.spanners.extend(tweaks)
        strings = []
        strings.append(r'\repeatTie')
        bundle.after.spanners.extend(strings)
        return bundle

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
