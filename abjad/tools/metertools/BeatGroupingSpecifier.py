# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject
from abjad.tools import sequencetools


class BeatGroupingSpecifier(AbjadValueObject):
    r'''Beat grouping specifier.

    Beat grouping specifier models different ways that a conductor might
    chose to group together the beats of a measure.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_fuse_remainder',
        '_remainder_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        counts=None,
        fuse_remainder=False,
        remainder_direction=Right,
        ):
        self._counts = counts
        self._fuse_remainder = fuse_remainder
        self._remainder_direction = remainder_direction

    ### SPECIAL METHODS ###

    def __call__(self, beats):
        r'''Calls beat grouping specifier on `beats`.

        ..  container:: example

            **Example 1.** Groups beats into pairs:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=[2],
                ...     )
                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

        ..  container:: example

            **Example 2.** Groups beats into groups of three:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=[3],
                ...     )
                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [3, 3]

        Returns list of beat lists.
        '''
        assert isinstance(beats, (list, tuple)), repr(beats)
        if self.counts is None:
            beat_group = list(beats)
            beat_groups = [beat_group]
            return beat_groups
        beat_groups = sequencetools.partition_sequence_by_counts(
            beats,
            counts=self.counts,
            cyclic=True,
            overhang=False,
            )
        beats_included = sum([len(_) for _ in beat_groups])
        if beats_included == len(beats):
            return beat_groups
        remainder_length = len(beats) - beats_included
        if self.remainder_direction == Left:
            beat_groups = sequencetools.partition_sequence_by_counts(
                beats[remainder_length:],
                counts=self.counts,
                cyclic=True,
                overhang=False
                )
            remainder = beats[:remainder_length]
            if self.fuse_remainder:
                beat_groups[0] = remainder + beat_groups[0]
            else:
                beat_groups.insert(0, remainder)
        else:
            beat_groups = sequencetools.partition_sequence_by_counts(
                beats[:-remainder_length],
                counts=self.counts,
                cyclic=True,
                overhang=False
                )
            remainder = beats[-remainder_length:]
            if self.fuse_remainder:
                beat_groups[-1] = beat_groups[-1] + remainder
            else:
                beat_groups.append(remainder)
        return beat_groups

    def __format__(self, format_specification=''):
        r'''Formats beat grouping specifier.

        ..  container:: example

            ::

                >>> specifier = metertools.BeatGroupingSpecifier()
                >>> print(format(specifier))
                metertools.BeatGroupingSpecifier(
                    fuse_remainder=False,
                    remainder_direction=Right,
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __repr__(self):
        r'''Gets interpreter representation of beat grouping specifier.

        ..  container:: example

            ::

                >>> metertools.BeatGroupingSpecifier()
                BeatGroupingSpecifier(fuse_remainder=False, remainder_direction=Right)

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of beat grouping specifier.

        ..  container:: example

            **Example 1.** Groups beats into a single group:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=None,
                ...     )
                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [6]

        ..  container:: example

            **Example 1.** Groups beats into pairs:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=[2],
                ...     )
                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

        ..  container:: example

            **Example 2.** Groups beats into groups of three:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=[3],
                ...     )
                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [3, 3]

        Defaults to none.

        Set to positive integers or none.
        '''
        return self._counts

    @property
    def fuse_remainder(self):
        r'''Is true when remainder beat group should fuse to next closest beat
        group. Otherwise false.

        ..  container:: example

            **Example 1.** Groups beats into pairs. Remainder at right.
            Does not fuse remainder:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=[2],
                ...     fuse_remainder=False,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beats = 5 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beats = 7 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

            ::

                >>> beats = 8 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beats = 9 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2, 1]

            This is default behavior.

        ..  container:: example

            **Example 2.** Groups beats into groups of two. Remainder at right.
            Fuses remainder to nearest group:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=[2],
                ...     fuse_remainder=True,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beats = 5 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 3]

            ::

                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beats = 7 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 3]

            ::

                >>> beats = 8 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beats = 9 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 3]

        Defaults to false.

        Set to true or false.
        '''
        return self._fuse_remainder

    @property
    def remainder_direction(self):
        r'''Gets remainder direction of beat grouping specifier.

        ..  container:: example

            **Example 1a.** Groups beats into pairs. Remainder at right:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=[2],
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beats = 4 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2]

            ::

                >>> beats = 5 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beats = 7 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

        ..  container:: example

            **Example 1b.** Groups beats into pairs. Remainder at left:

            ::

                >>> specifier = metertools.BeatGroupingSpecifier(
                ...     counts=[2],
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> beats = 4 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2]

            ::

                >>> beats = 5 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [1, 2, 2]

            ::

                >>> beats = 6 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beats = 7 * [Duration(1, 4)]
                >>> specifier(beats)
                [[Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [1, 2, 2, 2]

        Defaults to right.

        Set to right or left.
        '''
        return self._remainder_direction