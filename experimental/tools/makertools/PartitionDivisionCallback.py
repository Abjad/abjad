# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject


class PartitionDivisionCallback(AbjadValueObject):
    r'''Partition division callback.

    ..  container:: example

        Division lists for examples:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> division_maker = division_maker.split_by_durations(
            ...     compound_meter_multiplier=Multiplier(3, 2),
            ...     durations=[(1, 4)],
            ...     )
            >>> meters = [
            ...     metertools.Meter((4, 4)),
            ...     metertools.Meter((5, 4)),
            ...     metertools.Meter((6, 4)),
            ...     metertools.Meter((7, 4)),
            ...     ]
            >>> beat_lists = division_maker(meters)
            >>> for beat_list in beat_lists:
            ...     beat_list
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))]
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))]
            [Division((3, 8)), Division((3, 8)), Division((3, 8)), Division((3, 8))]
            [Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))]

    ..  container:: example

        **Example 1a.** Beat lists grouped in pairs. Remainder at right:

        ::

            >>> callback = makertools.PartitionDivisionCallback(
            ...     counts=[2],
            ...     append_remainder=False,
            ...     remainder_direction=Right,
            ...     )
            >>> grouped_beat_lists = callback(beat_lists)
            >>> for grouped_beat_list in grouped_beat_lists:
            ...     grouped_beat_list
            [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
            [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
            [[Division((3, 8)), Division((3, 8))], [Division((3, 8)), Division((3, 8))]]
            [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]

        **Example 1b.** Beat lists grouped in pairs. Remainder fused at right:

        ::

            >>> callback = makertools.PartitionDivisionCallback(
            ...     counts=[2],
            ...     append_remainder=True,
            ...     remainder_direction=Right,
            ...     )
            >>> grouped_beat_lists = callback(beat_lists)
            >>> for grouped_beat_list in grouped_beat_lists:
            ...     grouped_beat_list
            [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
            [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4)), Division((1, 4))]]
            [[Division((3, 8)), Division((3, 8))], [Division((3, 8)), Division((3, 8))]]
            [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4)), Division((1, 4))]]

    ..  container:: example

        **Example 2a.** Beat lists grouped in pairs. Remainder at left:

        ::

            >>> callback = makertools.PartitionDivisionCallback(
            ...     counts=[2],
            ...     append_remainder=False,
            ...     remainder_direction=Left,
            ...     )
            >>> grouped_beat_lists = callback(beat_lists)
            >>> for grouped_beat_list in grouped_beat_lists:
            ...     grouped_beat_list
            [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
            [[Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
            [[Division((3, 8)), Division((3, 8))], [Division((3, 8)), Division((3, 8))]]
            [[Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]

        **Example 1b.** Beat lists grouped in pairs. Remainder fused at left:

        ::

            >>> callback = makertools.PartitionDivisionCallback(
            ...     counts=[2],
            ...     append_remainder=True,
            ...     remainder_direction=Left,
            ...     )
            >>> grouped_beat_lists = callback(beat_lists)
            >>> for grouped_beat_list in grouped_beat_lists:
            ...     grouped_beat_list
            [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
            [[Division((1, 4)), Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
            [[Division((3, 8)), Division((3, 8))], [Division((3, 8)), Division((3, 8))]]
            [[Division((1, 4)), Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]

    Groups beats into conductors' groups.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_fuse_assignable_total_duration',
        '_append_remainder',
        '_remainder_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        counts=None,
        fuse_assignable_total_duration=False,
        append_remainder=False,
        remainder_direction=Right,
        ):
        self._counts = counts
        self._fuse_assignable_total_duration = fuse_assignable_total_duration
        self._append_remainder = append_remainder
        self._remainder_direction = remainder_direction

    ### SPECIAL METHODS ###

    def __call__(self, divisions):
        r'''Calls partition division callback on `divisions`.

        ..  container:: example

            **Example 1.** Groups beat list elements into pairs:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     )
                >>> division = 6 * [(1, 4)]
                >>> grouped_divisions = callback([division])
                >>> grouped_divisions[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

        ..  container:: example

            **Example 2.** Groups beat list elements into groups of three:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[3],
                ...     )
                >>> division = 6 * [(1, 4)]
                >>> grouped_divisions = callback([division])
                >>> grouped_divisions[0]
                [[Division((1, 4)), Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [3, 3]

        ..  container:: example

            **Example 3.** Works with start offset:

            ::

                >>> callback = makertools.PartitionDivisionCallback(counts=[3])
                >>> divisions = 6 * [durationtools.Division((1, 4))]
                >>> divisions[0]._start_offset = Offset(1, 4)

            ::

                >>> division_lists = callback(divisions)
                >>> len(division_lists)
                2

            ::

                >>> for division in division_lists[0]:
                ...     division
                Division((1, 4), start_offset=Offset(1, 4))
                Division((1, 4), start_offset=Offset(1, 2))
                Division((1, 4), start_offset=Offset(3, 4))

            ::

                >>> for division in division_lists[1]:
                ...     division
                Division((1, 4), start_offset=Offset(1, 1))
                Division((1, 4), start_offset=Offset(5, 4))
                Division((1, 4), start_offset=Offset(3, 2))

        Returns list of division lists.
        '''
        from experimental import makertools
        grouped_divisions = []
        divisions, start_offset = makertools.DivisionMaker._to_divisions(
            divisions)
        if divisions and isinstance(divisions[0], list):
            start_offset = divisions[0][0].start_offset
            for division in divisions:
                grouped_division = \
                    self._beat_list_to_grouped_beat_list(division)
                grouped_divisions.append(grouped_division)
            result = grouped_divisions
        else:
            start_offset = divisions[0].start_offset
            grouped_division = \
                self._beat_list_to_grouped_beat_list(divisions)
            result = grouped_division
        result, start_offset = makertools.DivisionMaker._to_divisions(
            result,
            start_offset=start_offset,
            )
        return result

    def _beat_list_to_grouped_beat_list(self, beat_list):
        assert isinstance(beat_list, (list, tuple)), repr(beat_list)
        beat_list_ = []
        for beat in beat_list:
            if hasattr(beat, 'duration'):
                beat = durationtools.Division(beat.duration)
            else:
                beat = durationtools.Division(beat)
            beat_list_.append(beat)
        beat_list = beat_list_
        total_duration = sum(beat_list)
        total_duration = durationtools.Duration(total_duration)
        if (total_duration.is_assignable and 
            self.fuse_assignable_total_duration):
            return [[durationtools.Division(total_duration)]]
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
            if self.append_remainder:
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
            if self.append_remainder:
                grouped_beat_list[-1] = grouped_beat_list[-1] + remainder
            else:
                grouped_beat_list.append(remainder)
        return grouped_beat_list

    def __format__(self, format_specification=''):
        r'''Formats beat callback.

        ..  container:: example

            ::

                >>> callback = makertools.PartitionDivisionCallback()
                >>> print(format(callback))
                makertools.PartitionDivisionCallback(
                    fuse_assignable_total_duration=False,
                    append_remainder=False,
                    remainder_direction=Right,
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __repr__(self):
        r'''Gets interpreter representation of beat callback.

        ..  container:: example

            ::

                >>> makertools.PartitionDivisionCallback()
                PartitionDivisionCallback(fuse_assignable_total_duration=False, append_remainder=False, remainder_direction=Right)

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of beat callback.

        ..  container:: example

            **Example 1.** Groups beats into a single group:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=None,
                ...     )
                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [6]

        ..  container:: example

            **Example 1.** Groups beats into pairs:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     )
                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

        ..  container:: example

            **Example 2.** Groups beats into groups of three:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[3],
                ...     )
                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [3, 3]

        Defaults to none.

        Set to positive integers or none.
        '''
        return self._counts

    @property
    def fuse_assignable_total_duration(self):
        r'''Is true when assignable total duration of all input beats should
        be fused into a single duration. Otherwise false.

        ..  container:: example

            **Example 1.** Groups beats into pairs. Does not fuse assignable
            total durations:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     fuse_assignable_total_duration=False,
                ...     )

            ::

                >>> beat_list = 5 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

            ::

                >>> beat_list = 8 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beat_list = 9 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2, 1]

        ..  container:: example

            **Example 2.** Groups beats into pairs. Fuse assignable total
            durations:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     fuse_assignable_total_duration=True,
                ...     )

            ::

                >>> beat_list = 5 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((3, 2))]]
                >>> [len(beat_group) for beat_group in _]
                [1]

            ::

                >>> beat_list = 7 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((7, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [1]

            ::

                >>> beat_list = 8 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((2, 1))]]
                >>> [len(beat_group) for beat_group in _]
                [1]

            ::

                >>> beat_list = 9 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2, 1]

        Overrides all other settings when total duration is assignable.

        Defaults to false.

        Set to true or false.
        '''
        return self._fuse_assignable_total_duration

    @property
    def append_remainder(self):
        r'''Is true when remainder beat group should fuse to next closest beat
        group. Otherwise false.

        ..  container:: example

            **Example 1.** Groups beats into pairs. Remainder at right.
            Does not fuse remainder:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     append_remainder=False,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 5 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

            ::

                >>> beat_list = 8 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beat_list = 9 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2, 1]

        ..  container:: example

            **Example 2.** Groups beats into groups of two. Remainder at right.
            Fuses remainder to nearest group:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     append_remainder=True,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 5 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 3]

            ::

                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 3]

            ::

                >>> beat_list = 8 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beat_list = 9 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 3]

        Defaults to false.

        Set to true or false.
        '''
        return self._append_remainder

    @property
    def remainder_direction(self):
        r'''Gets remainder direction of beat callback.

        ..  container:: example

            **Example 1a.** Groups beats into pairs. Remainder at right:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 4 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2]

            ::

                >>> beat_list = 5 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

        ..  container:: example

            **Example 1b.** Groups beats into pairs. Remainder at left:

            ::

                >>> callback = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> beat_list = 4 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2]

            ::

                >>> beat_list = 5 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [1, 2, 2]

            ::

                >>> beat_list = 6 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [(1, 4)]
                >>> grouped_beat_lists = callback([beat_list])
                >>> grouped_beat_lists[0]
                [[Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))], [Division((1, 4)), Division((1, 4))]]
                >>> [len(beat_group) for beat_group in _]
                [1, 2, 2, 2]

        Defaults to right.

        Set to right or left.
        '''
        return self._remainder_direction