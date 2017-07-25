# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class Tuning(AbjadValueObject):
    r'''Tuning.

    ::

        >>> import abjad

    ..  container:: example

        Violin tuning:

        ::

            >>> indicator = abjad.Tuning(
            ...     pitches=('G3', 'D4', 'A4', 'E5'),
            ...     )
            >>> f(indicator)
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitches',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pitches=None,
        ):
        from abjad.tools import pitchtools
        if pitches is not None:
            if isinstance(pitches, type(self)):
                pitches = pitches.pitches
            else:
                pitches = pitchtools.PitchSegment(
                    items=pitches,
                    item_class=pitchtools.NamedPitch,
                    )
        self._pitches = pitches

    ### PUBLIC METHODS ###

    def get_pitch_ranges_by_string_number(self, string_number):
        r'''Gets tuning pitch ranges by string number.

        ..  container:: example

            Violin tuning:

            ::

                >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
                >>> string_number = abjad.StringNumber((2, 3))
                >>> tuning.get_pitch_ranges_by_string_number(string_number)
                (PitchRange('[A4, A6]'), PitchRange('[D4, D6]'))

        Returns pitch ranges.
        '''
        from abjad.tools import indicatortools
        string_number = indicatortools.StringNumber(string_number)
        pitch_ranges = self.pitch_ranges
        result = []
        for number in string_number.numbers:
            index = -number
            pitch_range = pitch_ranges[index]
            result.append(pitch_range)
        return tuple(result)

    def get_pitches_by_string_number(self, string_number):
        r'''Gets tuning pitches by string number.

        ..  container:: example

            Violin tuning:

            ::

                >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
                >>> string_number = abjad.StringNumber((2, 3))
                >>> tuning.get_pitches_by_string_number(string_number)
                (NamedPitch("a'"), NamedPitch("d'"))

        Returns named pitches.
        '''
        from abjad.tools import indicatortools
        string_number = indicatortools.StringNumber(string_number)
        result = []
        for number in string_number.numbers:
            index = -number
            pitch = self.pitches[index]
            result.append(pitch)
        return tuple(result)

    def voice_pitch_classes(
        self,
        pitch_classes,
        allow_open_strings=True,
        ):
        r"""Voices `pitch_classes`.

        ..  container:: example

            ::

                >>> tuning = abjad.Tuning(('G3', 'D4', 'A4', 'E5'))
                >>> voicings = tuning.voice_pitch_classes(('a',))
                >>> for voicing in voicings:
                ...     voicing
                ...
                (None, None, None, NamedPitch("a''"))
                (None, None, None, NamedPitch("a'''"))
                (None, None, NamedPitch("a'"), None)
                (None, None, NamedPitch("a''"), None)
                (None, None, NamedPitch("a'''"), None)
                (None, NamedPitch("a'"), None, None)
                (None, NamedPitch("a''"), None, None)
                (NamedPitch('a'), None, None, None)
                (NamedPitch("a'"), None, None, None)

            ::

                >>> voicings = tuning.voice_pitch_classes(
                ...     ('a', 'd'),
                ...     allow_open_strings=False,
                ...     )
                >>> for voicing in voicings:
                ...     voicing
                ...
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
                (NamedPitch('a'), None, None, NamedPitch("d'''"))
                (NamedPitch('a'), None, None, NamedPitch("d''''"))
                (NamedPitch('a'), None, NamedPitch("d''"), None)
                (NamedPitch('a'), None, NamedPitch("d'''"), None)
                (NamedPitch('a'), NamedPitch("d''"), None, None)
                (NamedPitch('a'), NamedPitch("d'''"), None, None)
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

        Returns tuple of sequences.
        """
        import abjad
        pitch_classes = [abjad.NamedPitchClass(_) for _ in pitch_classes]
        pitch_classes.extend([None] * (len(self.pitches) - len(pitch_classes)))
        enumerator = abjad.Enumerator(pitch_classes)
        permutations = enumerator.yield_permutations()
        permutations = set([tuple(_) for _ in permutations])
        pitch_ranges = self.pitch_ranges
        result = []
        for permutation in permutations:
            sequences = []
            for pitch_range, pitch_class in zip(pitch_ranges, permutation):
                if pitch_class is None:
                    sequences.append([None])
                    continue
                pitches = pitch_range.voice_pitch_class(pitch_class)
                if not allow_open_strings:
                    pitches = [pitch for pitch in pitches
                        if pitch != pitch_range.start_pitch
                        ]
                if not pitches:
                    pitches = [None]
                sequences.append(pitches)
            enumerator = abjad.Enumerator(sequences)
            subresult = enumerator.yield_outer_product()
            subresult = [tuple(x) for x in subresult]
            result.extend(subresult)
        result.sort()
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def pitch_ranges(self):
        r'''Gets two-octave pitch-ranges for each pitch in this tuning.

        ..  container:: example

            ::

                >>> pitch_ranges = indicator.pitch_ranges
                >>> f(pitch_ranges)
                abjad.PitchRangeList(
                    [
                        abjad.PitchRange('[G3, G5]'),
                        abjad.PitchRange('[D4, D6]'),
                        abjad.PitchRange('[A4, A6]'),
                        abjad.PitchRange('[E5, E7]'),
                        ]
                    )

        Returns pitch-range list.
        '''
        from abjad.tools import pitchtools
        result = []
        for pitch in self.pitches:
            pitch_range = pitchtools.PitchRange.from_pitches(pitch, pitch + 24)
            result.append(pitch_range)
        result = pitchtools.PitchRangeList(result)
        return result

    @property
    def pitches(self):
        r'''Gets pitches of tuning.

        ..  container:: example

            ::

                >>> pitches = indicator.pitches
                >>> f(pitches)
                abjad.PitchSegment(
                    (
                        abjad.NamedPitch('g'),
                        abjad.NamedPitch("d'"),
                        abjad.NamedPitch("a'"),
                        abjad.NamedPitch("e''"),
                        ),
                    item_class=abjad.NamedPitch,
                    )

        Returns pitch segment.
        '''
        return self._pitches
