import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.StorageFormatManager import StorageFormatManager


class Tremolo(AbjadValueObject):
    r"""
    Tremolo (of exactly two notes).

    ..  container:: example

        With two beams:

        >>> chord = abjad.Chord("<cs' e'>4")
        >>> tremolo = abjad.Tremolo(beam_count=2)
        >>> abjad.attach(tremolo, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            \repeat tremolo 2
            {
            cs'16 e'16
            }

    ..  container:: example

        With three beams:

        >>> chord = abjad.Chord("<cs' e'>4")
        >>> tremolo = abjad.Tremolo(beam_count=3)
        >>> abjad.attach(tremolo, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            \repeat tremolo 4
            {
            cs'32 e'32
            }

    Tremolo affects the formatting of chords.

    Tremolo has no effect when attached to notes or rests.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_count',
        '_is_slurred',
        )

    _format_slot = None

    ### INITIALIZER ###

    def __init__(
        self,
        beam_count: int = 3,
        *,
        is_slurred: bool = None,
        ) -> None:
        assert isinstance(beam_count, int), repr(beam_count)
        assert 0 < beam_count, repr(beam_count)
        self._beam_count = beam_count
        if is_slurred is not None:
            is_slurred = bool(is_slurred)
        self._is_slurred = is_slurred

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments) -> 'Tremolo':
        """
        Copies tremolo.

        ..  container:: example

            Copies tremolo:

            >>> import copy
            >>> tremolo_1 = abjad.Tremolo(beam_count=2)
            >>> tremolo_2 = copy.copy(tremolo_1)

            >>> tremolo_1 == tremolo_2
            True

            >>> tremolo_1 is not tremolo_2
            True

        """
        return super().__copy__(*arguments)

    def __format__(self, format_specification='') -> str:
        """
        Formats stem tremolo.

        ..  container:: example

            With two beams:

            >>> tremolo = abjad.Tremolo(beam_count=2)
            >>> print(format(tremolo))
            abjad.Tremolo(
                beam_count=2,
                )

        ..  container:: example

            With three beams:

            >>> tremolo = abjad.Tremolo(beam_count=3)
            >>> print(format(tremolo))
            abjad.Tremolo(
                beam_count=3,
                )

        """
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        assert format_specification == 'lilypond'
        raise Exception('no LilyPond format available.')

    def __str__(self) -> str:
        """
        Gets string representation of tremolo.

        ..  container:: example

            >>> tremolo = abjad.Tremolo(beam_count=2)
            >>> str(tremolo)
            'Tremolo(beam_count=2)'

            >>> tremolo = abjad.Tremolo(beam_count=3)
            >>> str(tremolo)
            'Tremolo(beam_count=3)'

        """
        return super().__str__()

    ### PUBLIC PROPERTIES ###

    @property
    def beam_count(self) -> int:
        r"""
        Gets beam count of tremolo.

        ..  container:: example

            With two beams:

            >>> chord = abjad.Chord("<cs' e'>4")
            >>> tremolo = abjad.Tremolo(beam_count=2)
            >>> abjad.attach(tremolo, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \repeat tremolo 2
                {
                cs'16 e'16
                }

        ..  container:: example

            With three beams:

            >>> chord = abjad.Chord("<cs' e'>4")
            >>> tremolo = abjad.Tremolo()
            >>> abjad.attach(tremolo, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \repeat tremolo 4
                {
                cs'32 e'32
                }

        """
        return self._beam_count

    @property
    def is_slurred(self) -> typing.Optional[bool]:
        r"""
        Is true when tremolo is slurred.

        ..  container:: example

            Without slur:

            >>> chord = abjad.Chord("<cs' e'>4")
            >>> tremolo = abjad.Tremolo()
            >>> abjad.attach(tremolo, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \repeat tremolo 4
                {
                cs'32 e'32
                }

        ..  container:: example

            With slur:

            >>> chord = abjad.Chord("<cs' e'>4")
            >>> tremolo = abjad.Tremolo(is_slurred=True)
            >>> abjad.attach(tremolo, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \repeat tremolo 4
                {
                cs'32 \( e'32 \)
                }

        """
        return self._is_slurred

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on tremolo.
        
        The LilyPond ``\repeat tremolo`` command refuses tweaks.

        Override the LilyPond ``Beam`` grob instead.
        """
        pass
