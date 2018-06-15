import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.mathtools.Enumerator import Enumerator
from abjad.pitch.NamedPitch import NamedPitch
from abjad.pitch.NamedPitchClass import NamedPitchClass
from abjad.pitch.PitchRange import PitchRange
from abjad.pitch.PitchSegment import PitchSegment
from .StringNumber import StringNumber


class Tuning(AbjadValueObject):
    """
    Tuning.

    ..  container:: example

        Violin tuning:

        >>> indicator = abjad.Tuning(pitches=('G3', 'D4', 'A4', 'E5'))
        >>> abjad.f(indicator)
        abjad.Tuning(
            pitches=abjad.PitchSegment(
                (
                    abjad.NamedPitch('g'),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("a'"),
                    abjad.NamedPitch("e''"),
                    ),
                item_class=abjad.NamedPitch,
                ),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitches',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pitches: typing.Union['Tuning', typing.Iterable] = None,
        ) -> None:
        if pitches is not None:
            if isinstance(pitches, type(self)):
                pitches = pitches.pitches
            pitches = PitchSegment(
                items=pitches,
                item_class=NamedPitch,
                )
        self._pitches: typing.Optional[PitchSegment] = pitches

    ### PUBLIC PROPERTIES ###

    @property
    def pitch_ranges(self) -> typing.List[PitchRange]:
        """
        Gets two-octave pitch-ranges for each pitch in this tuning.

        ..  container:: example

            >>> indicator = abjad.Tuning(pitches=('G3', 'D4', 'A4', 'E5'))
            >>> for range_ in indicator.pitch_ranges:
            ...     range_
            PitchRange('[G3, G5]')
            PitchRange('[D4, D6]')
            PitchRange('[A4, A6]')
            PitchRange('[E5, E7]')

        """
        result = []
        for pitch in self.pitches or []:
            pitch_range = PitchRange.from_pitches(pitch, pitch + 24)
            result.append(pitch_range)
        return result

    @property
    def pitches(self) -> typing.Optional[PitchSegment]:
        """
        Gets pitches of tuning.

        ..  container:: example

            >>> indicator = abjad.Tuning(pitches=('G3', 'D4', 'A4', 'E5'))
            >>> pitches = indicator.pitches
            >>> abjad.f(pitches)
            abjad.PitchSegment(
                (
                    abjad.NamedPitch('g'),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("a'"),
                    abjad.NamedPitch("e''"),
                    ),
                item_class=abjad.NamedPitch,
                )

        """
        return self._pitches

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on tuning.
        """
        pass

    ### PUBLIC METHODS ###

    def get_pitch_ranges_by_string_number(
        self,
        string_number: StringNumber,
        ) -> typing.Tuple[PitchRange, ...]:
        """
        Gets tuning pitch ranges by string number.

        ..  container:: example

            Violin tuning:

            >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
            >>> string_number = abjad.StringNumber((2, 3))
            >>> tuning.get_pitch_ranges_by_string_number(string_number)
            (PitchRange('[A4, A6]'), PitchRange('[D4, D6]'))

        """
        if not isinstance(string_number, StringNumber):
            string_number = StringNumber(string_number)
        assert isinstance(string_number, StringNumber)
        pitch_ranges = self.pitch_ranges
        result = []
        for number in string_number.numbers:
            index = -number
            pitch_range = pitch_ranges[index]
            result.append(pitch_range)
        return tuple(result)

    def get_pitches_by_string_number(
        self,
        string_number: StringNumber,
        ) -> typing.Tuple[NamedPitch, ...]:
        """
        Gets tuning pitches by string number.

        ..  container:: example

            Violin tuning:

            >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
            >>> string_number = abjad.StringNumber((2, 3))
            >>> tuning.get_pitches_by_string_number(string_number)
            (NamedPitch("a'"), NamedPitch("d'"))

        """
        if not isinstance(string_number, StringNumber):
            string_number = StringNumber(string_number)
        assert isinstance(string_number, StringNumber)
        assert self.pitches is not None
        result = []
        for number in string_number.numbers:
            index = -number
            pitch = self.pitches[index]
            result.append(pitch)
        return tuple(result)

    def voice_pitch_classes(
        self,
        pitch_classes,
        allow_open_strings: bool = True,
        ):
        r"""
        Voices ``pitch_classes``.

        ..  container:: example

            >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
            >>> voicings = tuning.voice_pitch_classes(('a',))
            >>> for voicing in voicings:
            ...     voicing
            ...
            (NamedPitch('a'), None, None, None)
            (None, None, None, NamedPitch("a''"))
            (None, None, None, NamedPitch("a'''"))
            (None, None, NamedPitch("a'"), None)
            (None, None, NamedPitch("a''"), None)
            (None, None, NamedPitch("a'''"), None)
            (None, NamedPitch("a'"), None, None)
            (None, NamedPitch("a''"), None, None)
            (NamedPitch("a'"), None, None, None)

            >>> voicings = tuning.voice_pitch_classes(
            ...     ('a', 'd'),
            ...     allow_open_strings=False,
            ...     )
            >>> for voicing in voicings:
            ...     voicing
            ...
            (NamedPitch('a'), None, None, NamedPitch("d'''"))
            (NamedPitch('a'), None, None, NamedPitch("d''''"))
            (NamedPitch('a'), None, NamedPitch("d''"), None)
            (NamedPitch('a'), None, NamedPitch("d'''"), None)
            (NamedPitch('a'), NamedPitch("d''"), None, None)
            (NamedPitch('a'), NamedPitch("d'''"), None, None)
            (None, None, NamedPitch("d''"), NamedPitch("a''"))
            (None, None, NamedPitch("d''"), NamedPitch("a'''"))
            (None, None, NamedPitch("a''"), NamedPitch("d'''"))
            (None, None, NamedPitch("a''"), NamedPitch("d''''"))
            (None, None, NamedPitch("d'''"), NamedPitch("a''"))
            (None, None, NamedPitch("d'''"), NamedPitch("a'''"))
            (None, None, NamedPitch("a'''"), NamedPitch("d'''"))
            (None, None, NamedPitch("a'''"), NamedPitch("d''''"))
            (None, NamedPitch("a'"), None, NamedPitch("d'''"))
            (None, NamedPitch("a'"), None, NamedPitch("d''''"))
            (None, NamedPitch("a'"), NamedPitch("d''"), None)
            (None, NamedPitch("a'"), NamedPitch("d'''"), None)
            (None, NamedPitch("d''"), None, NamedPitch("a''"))
            (None, NamedPitch("d''"), None, NamedPitch("a'''"))
            (None, NamedPitch("d''"), NamedPitch("a''"), None)
            (None, NamedPitch("d''"), NamedPitch("a'''"), None)
            (None, NamedPitch("a''"), None, NamedPitch("d'''"))
            (None, NamedPitch("a''"), None, NamedPitch("d''''"))
            (None, NamedPitch("a''"), NamedPitch("d''"), None)
            (None, NamedPitch("a''"), NamedPitch("d'''"), None)
            (None, NamedPitch("d'''"), None, NamedPitch("a''"))
            (None, NamedPitch("d'''"), None, NamedPitch("a'''"))
            (None, NamedPitch("d'''"), NamedPitch("a''"), None)
            (None, NamedPitch("d'''"), NamedPitch("a'''"), None)
            (NamedPitch("d'"), None, None, NamedPitch("a''"))
            (NamedPitch("d'"), None, None, NamedPitch("a'''"))
            (NamedPitch("d'"), None, NamedPitch("a''"), None)
            (NamedPitch("d'"), None, NamedPitch("a'''"), None)
            (NamedPitch("d'"), NamedPitch("a'"), None, None)
            (NamedPitch("d'"), NamedPitch("a''"), None, None)
            (NamedPitch("a'"), None, None, NamedPitch("d'''"))
            (NamedPitch("a'"), None, None, NamedPitch("d''''"))
            (NamedPitch("a'"), None, NamedPitch("d''"), None)
            (NamedPitch("a'"), None, NamedPitch("d'''"), None)
            (NamedPitch("a'"), NamedPitch("d''"), None, None)
            (NamedPitch("a'"), NamedPitch("d'''"), None, None)
            (NamedPitch("d''"), None, None, NamedPitch("a''"))
            (NamedPitch("d''"), None, None, NamedPitch("a'''"))
            (NamedPitch("d''"), None, NamedPitch("a''"), None)
            (NamedPitch("d''"), None, NamedPitch("a'''"), None)
            (NamedPitch("d''"), NamedPitch("a'"), None, None)
            (NamedPitch("d''"), NamedPitch("a''"), None, None)

        """
        assert self.pitches is not None
        pitch_classes = [NamedPitchClass(_) for _ in pitch_classes]
        pitch_classes.extend([None] * (len(self.pitches) - len(pitch_classes)))
        enumerator = Enumerator(pitch_classes)
        permutations = enumerator.yield_permutations()
        permutations = set([tuple(_) for _ in permutations])
        pitch_ranges = self.pitch_ranges
        result: typing.List[
            typing.Tuple[typing.Union[NamedPitch, None], ...]
            ] = []
        for permutation in permutations:
            sequences = []
            for pitch_range, pitch_class in zip(pitch_ranges, permutation):
                if pitch_class is None:
                    sequences.append([None])
                    continue
                pitches = pitch_range.voice_pitch_class(pitch_class)
                if not allow_open_strings:
                    pitches = [
                        pitch for pitch in pitches
                        if pitch != pitch_range.start_pitch
                        ]
                if not pitches:
                    pitches = [None]
                sequences.append(pitches)
            enumerator = Enumerator(sequences)
            subresult = enumerator.yield_outer_product()
            subresult = [tuple(x) for x in subresult]
            result.extend(subresult)
        result.sort()
        return tuple(result)
