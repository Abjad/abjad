# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject


class Tuning(AbjadValueObject):
    r'''Tuning indicator.

    ..  container:: example

        **Example 1.** Violin tuning:

        ::

            >>> indicator = indicatortools.Tuning(
            ...     pitches=('G3', 'D4', 'A4', 'E5'),
            ...     )
            >>> print(format(indicator))
            indicatortools.Tuning(
                pitches=pitchtools.PitchSegment(
                    (
                        pitchtools.NamedPitch('g'),
                        pitchtools.NamedPitch("d'"),
                        pitchtools.NamedPitch("a'"),
                        pitchtools.NamedPitch("e''"),
                        ),
                    item_class=pitchtools.NamedPitch,
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_pitches',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pitches=None,
        ):
        from abjad.tools import pitchtools
        self._default_scope = None
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

            **Example 1.** Violin tuning:

            ::

                >>> tuning = indicatortools.Tuning(('G3', 'D4', 'A4', 'E5'))
                >>> string_number = indicatortools.StringNumber((2, 3))
                >>> tuning.get_pitch_ranges_by_string_number(string_number)
                (PitchRange(range_string='[A4, A6]'), PitchRange(range_string='[D4, D6]'))

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

            **Example 1.** Violin tuning:

            ::

                >>> tuning = indicatortools.Tuning(('G3', 'D4', 'A4', 'E5'))
                >>> string_number = indicatortools.StringNumber((2, 3))
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

            **Example 1.**

            ::

                >>> tuning = indicatortools.Tuning(('G3', 'D4', 'A4', 'E5'))
                >>> voicings = tuning.voice_pitch_classes(('a',))
                >>> for voicing in voicings:
                ...     voicing
                ...
                (NamedPitch('a'), None, None, None)
                (NamedPitch("a'"), None, None, None)
                (None, NamedPitch("a'"), None, None)
                (None, NamedPitch("a''"), None, None)
                (None, None, NamedPitch("a'"), None)
                (None, None, NamedPitch("a''"), None)
                (None, None, NamedPitch("a'''"), None)
                (None, None, None, NamedPitch("a''"))
                (None, None, None, NamedPitch("a'''"))

            ::

                >>> voicings = tuning.voice_pitch_classes(
                ...     ('a', 'd'),
                ...     allow_open_strings=False,
                ...     )
                >>> for voicing in voicings:
                ...     voicing
                ...
                (NamedPitch('a'), NamedPitch("d''"), None, None)
                (NamedPitch('a'), NamedPitch("d'''"), None, None)
                (NamedPitch('a'), None, NamedPitch("d''"), None)
                (NamedPitch('a'), None, NamedPitch("d'''"), None)
                (NamedPitch('a'), None, None, NamedPitch("d'''"))
                (NamedPitch('a'), None, None, NamedPitch("d''''"))
                (NamedPitch("d'"), NamedPitch("a'"), None, None)
                (NamedPitch("d'"), NamedPitch("a''"), None, None)
                (NamedPitch("d'"), None, NamedPitch("a''"), None)
                (NamedPitch("d'"), None, NamedPitch("a'''"), None)
                (NamedPitch("d'"), None, None, NamedPitch("a''"))
                (NamedPitch("d'"), None, None, NamedPitch("a'''"))
                (NamedPitch("a'"), NamedPitch("d''"), None, None)
                (NamedPitch("a'"), NamedPitch("d'''"), None, None)
                (NamedPitch("a'"), None, NamedPitch("d''"), None)
                (NamedPitch("a'"), None, NamedPitch("d'''"), None)
                (NamedPitch("a'"), None, None, NamedPitch("d'''"))
                (NamedPitch("a'"), None, None, NamedPitch("d''''"))
                (NamedPitch("d''"), NamedPitch("a'"), None, None)
                (NamedPitch("d''"), NamedPitch("a''"), None, None)
                (NamedPitch("d''"), None, NamedPitch("a''"), None)
                (NamedPitch("d''"), None, NamedPitch("a'''"), None)
                (NamedPitch("d''"), None, None, NamedPitch("a''"))
                (NamedPitch("d''"), None, None, NamedPitch("a'''"))
                (None, NamedPitch("a'"), NamedPitch("d''"), None)
                (None, NamedPitch("a'"), NamedPitch("d'''"), None)
                (None, NamedPitch("a'"), None, NamedPitch("d'''"))
                (None, NamedPitch("a'"), None, NamedPitch("d''''"))
                (None, NamedPitch("d''"), NamedPitch("a''"), None)
                (None, NamedPitch("d''"), NamedPitch("a'''"), None)
                (None, NamedPitch("d''"), None, NamedPitch("a''"))
                (None, NamedPitch("d''"), None, NamedPitch("a'''"))
                (None, NamedPitch("a''"), NamedPitch("d''"), None)
                (None, NamedPitch("a''"), NamedPitch("d'''"), None)
                (None, NamedPitch("a''"), None, NamedPitch("d'''"))
                (None, NamedPitch("a''"), None, NamedPitch("d''''"))
                (None, NamedPitch("d'''"), NamedPitch("a''"), None)
                (None, NamedPitch("d'''"), NamedPitch("a'''"), None)
                (None, NamedPitch("d'''"), None, NamedPitch("a''"))
                (None, NamedPitch("d'''"), None, NamedPitch("a'''"))
                (None, None, NamedPitch("d''"), NamedPitch("a''"))
                (None, None, NamedPitch("d''"), NamedPitch("a'''"))
                (None, None, NamedPitch("a''"), NamedPitch("d'''"))
                (None, None, NamedPitch("a''"), NamedPitch("d''''"))
                (None, None, NamedPitch("d'''"), NamedPitch("a''"))
                (None, None, NamedPitch("d'''"), NamedPitch("a'''"))
                (None, None, NamedPitch("a'''"), NamedPitch("d'''"))
                (None, None, NamedPitch("a'''"), NamedPitch("d''''"))

        Returns tuple of sequences.
        """
        from abjad.tools import pitchtools
        pitch_classes = [pitchtools.NamedPitchClass(x) for x in pitch_classes]
        pitch_classes.extend([None] * (len(self.pitches) - len(pitch_classes)))
        permutations = set([
            tuple(x) for x in
            sequencetools.yield_all_permutations_of_sequence(pitch_classes)
            ])
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
            subresult = sequencetools.yield_outer_product_of_sequences(
                sequences)
            subresult = [tuple(x) for x in subresult]
            result.extend(subresult)
        result.sort()
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of tuning.

        ..  container:: example

            **Example 1.** Violin tuning

            ::

                >>> indicator = indicatortools.Tuning(
                ...     pitches=('G3', 'D4', 'A4', 'E5'),
                ...     )
                >>> indicator.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope

    @property
    def pitch_ranges(self):
        r'''Gets two-octave pitch-ranges for each pitch in this tuning.

        ..  container:: example

            **Example 1.**

            ::

                >>> pitch_ranges = indicator.pitch_ranges
                >>> print(format(pitch_ranges))
                pitchtools.PitchRangeInventory(
                    [
                        pitchtools.PitchRange(
                            range_string='[G3, G5]',
                            ),
                        pitchtools.PitchRange(
                            range_string='[D4, D6]',
                            ),
                        pitchtools.PitchRange(
                            range_string='[A4, A6]',
                            ),
                        pitchtools.PitchRange(
                            range_string='[E5, E7]',
                            ),
                        ]
                    )

        Returns pitch-range inventory.
        '''
        from abjad.tools import pitchtools
        result = []
        for pitch in self.pitches:
            pitch_range = pitchtools.PitchRange.from_pitches(pitch, pitch + 24)
            result.append(pitch_range)
        result = pitchtools.PitchRangeInventory(result)
        return result

    @property
    def pitches(self):
        r'''Gets pitches of tuning.

        ..  container:: example

            **Example 1.**

            ::

                >>> pitches = indicator.pitches
                >>> print(format(pitches))
                pitchtools.PitchSegment(
                    (
                        pitchtools.NamedPitch('g'),
                        pitchtools.NamedPitch("d'"),
                        pitchtools.NamedPitch("a'"),
                        pitchtools.NamedPitch("e''"),
                        ),
                    item_class=pitchtools.NamedPitch,
                    )

        Returns pitch segment.
        '''
        return self._pitches
