# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject
from abjad.tools import sequencetools


class BeatGrouper(AbjadValueObject):
    r'''Beat grouper.

    ..  container:: example

        **Example 1.**

        ::

            >>> beat_maker = rhythmmakertools.DurationBeatMaker(
            ...     compound_beat_duration=Duration(3, 8),
            ...     simple_beat_duration=Duration(1, 4),
            ...     )

    Groups beats into conductors' groups.
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

    def __call__(self, beat_lists):
        r'''Calls beat grouper on `beat_lists`.

        ..  container:: example

            **Example 1.** Groups beat list elements into pairs:

            ::

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=[2],
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

        ..  container:: example

            **Example 2.** Groups beat list elements into groups of three:

            ::

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=[3],
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [3, 3]

        Returns list of beat lists.
        '''
        grouped_beat_lists = []
        for beat_list in beat_lists:
            grouped_beat_list = self._beat_list_to_grouped_beat_list(beat_list)
            grouped_beat_lists.append(grouped_beat_list)
        return grouped_beat_lists

    def _beat_list_to_grouped_beat_list(self, beat_list):
        assert isinstance(beat_list, (list, tuple)), repr(beat_list)
        if self.counts is None:
            beat_group = list(beat_list)
            grouped_beat_list = [beat_group]
            return grouped_beat_list
        grouped_beat_list = sequencetools.partition_sequence_by_counts(
            beat_list,
            counts=self.counts,
            cyclic=True,
            overhang=False,
            )
        beats_included = sum([len(_) for _ in grouped_beat_list])
        if beats_included == len(beat_list):
            return grouped_beat_list
        remainder_length = len(beat_list) - beats_included
        if self.remainder_direction == Left:
            grouped_beat_list = sequencetools.partition_sequence_by_counts(
                beat_list[remainder_length:],
                counts=self.counts,
                cyclic=True,
                overhang=False
                )
            remainder = beat_list[:remainder_length]
            if self.fuse_remainder:
                grouped_beat_list[0] = remainder + grouped_beat_list[0]
            else:
                grouped_beat_list.insert(0, remainder)
        else:
            grouped_beat_list = sequencetools.partition_sequence_by_counts(
                beat_list[:-remainder_length],
                counts=self.counts,
                cyclic=True,
                overhang=False
                )
            remainder = beat_list[-remainder_length:]
            if self.fuse_remainder:
                grouped_beat_list[-1] = grouped_beat_list[-1] + remainder
            else:
                grouped_beat_list.append(remainder)
        return grouped_beat_list

    def __format__(self, format_specification=''):
        r'''Formats beat grouper.

        ..  container:: example

            ::

                >>> grouper = rhythmmakertools.BeatGrouper()
                >>> print(format(grouper))
                rhythmmakertools.BeatGrouper(
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
        r'''Gets interpreter representation of beat grouper.

        ..  container:: example

            ::

                >>> rhythmmakertools.BeatGrouper()
                BeatGrouper(fuse_remainder=False, remainder_direction=Right)

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of beat grouper.

        ..  container:: example

            **Example 1.** Groups beats into a single group:

            ::

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=None,
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [6]

        ..  container:: example

            **Example 1.** Groups beats into pairs:

            ::

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=[2],
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

        ..  container:: example

            **Example 2.** Groups beats into groups of three:

            ::

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=[3],
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
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

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=[2],
                ...     fuse_remainder=False,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

            ::

                >>> beat_list = 8 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beat_list = 9 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2, 1]

        ..  container:: example

            **Example 2.** Groups beats into groups of two. Remainder at right.
            Fuses remainder to nearest group:

            ::

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=[2],
                ...     fuse_remainder=True,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 3]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 3]

            ::

                >>> beat_list = 8 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beat_list = 9 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 3]

        Defaults to false.

        Set to true or false.
        '''
        return self._fuse_remainder

    @property
    def remainder_direction(self):
        r'''Gets remainder direction of beat grouper.

        ..  container:: example

            **Example 1a.** Groups beats into pairs. Remainder at right:

            ::

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=[2],
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 4 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2]

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

        ..  container:: example

            **Example 1b.** Groups beats into pairs. Remainder at left:

            ::

                >>> grouper = rhythmmakertools.BeatGrouper(
                ...     counts=[2],
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> beat_list = 4 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2]

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [1, 2, 2]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [1, 2, 2, 2]

        Defaults to right.

        Set to right or left.
        '''
        return self._remainder_direction