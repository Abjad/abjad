import typing

from ..bundle import LilyPondFormatBundle
from ..storage import StorageFormatManager


class Ottava:
    r"""
    LilyPond ``\ottava`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> ottava = abjad.Ottava(n=1)
        >>> abjad.attach(ottava, staff[0])
        >>> ottava = abjad.Ottava(n=0, format_slot='after')
        >>> abjad.attach(ottava, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \ottava 1
                c'4
                d'4
                e'4
                f'4
                \ottava 0
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_format_slot", "_n")

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, n: int = None, *, format_slot: str = None) -> None:
        if n is not None:
            assert isinstance(n, int), repr(n)
        self._n = n
        if format_slot is not None:
            assert format_slot in ("before", "after"), repr(format_slot)
        self._format_slot = format_slot

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
        Delegates to storage format manager.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        n = self.n or 0
        string = rf"\ottava {n}"
        if self.format_slot in ("before", None):
            bundle.before.commands.append(string)
        else:
            assert self.format_slot == "after"
            bundle.after.commands.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def format_slot(self) -> typing.Optional[str]:
        r"""
        Gets format slot.

        ..  container:: example

            Format slot defaults to before:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> ottava = abjad.Ottava(n=1)
            >>> abjad.attach(ottava, staff[0])
            >>> ottava = abjad.Ottava(n=0)
            >>> abjad.attach(ottava, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \ottava 1
                    c'4
                    d'4
                    e'4
                    \ottava 0
                    f'4
                }

            Set format slot to after like this:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> ottava = abjad.Ottava(n=1)
            >>> abjad.attach(ottava, staff[0])
            >>> ottava = abjad.Ottava(n=0, format_slot='after')
            >>> abjad.attach(ottava, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \ottava 1
                    c'4
                    d'4
                    e'4
                    f'4
                    \ottava 0
                }

        """
        return self._format_slot

    @property
    def n(self) -> typing.Optional[int]:
        """
        Gets octave change.
        """
        return self._n

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.Ottava().persistent
            True

        Class constant.
        """
        return self._persistent
