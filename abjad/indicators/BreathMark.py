import typing

from .. import enums
from ..bundle import LilyPondFormatBundle
from ..overrides import TweakInterface
from ..storage import StorageFormatManager


class BreathMark:
    r"""
    Breath mark.

    ..  container:: example

        Attached to a single note:

        >>> note = abjad.Note("c'4")
        >>> breath_mark = abjad.BreathMark()
        >>> abjad.attach(breath_mark, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            \breathe

    ..  container:: example

        Attached to notes in a staff:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> abjad.beam(staff[:4])
        >>> abjad.beam(staff[4:])
        >>> abjad.attach(abjad.BreathMark(), staff[3])
        >>> abjad.attach(abjad.BreathMark(), staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

    ..  container:: example

        REGRESSION. Abjad parses LilyPond's ``\breathe`` command correctly:

        >>> staff = abjad.Staff(r"c'4 d' e' f' \breathe")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \breathe
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_tweaks",)

    _format_slot = "after"

    _time_orientation = enums.Right

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

    def __str__(self) -> str:
        r"""
        Gets string representation of breath mark.

        ..  container:: example

            >>> str(abjad.BreathMark())
            '\\breathe'

        """
        return r"\breathe"

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.after.articulations.extend(tweaks)
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> breath = abjad.BreathMark()
            >>> abjad.tweak(breath).color = "#blue"
            >>> abjad.attach(breath, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                \tweak color #blue
                \breathe

        """
        return self._tweaks
