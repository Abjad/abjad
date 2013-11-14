# -*- encoding: utf-8 -*-
import collections
import copy
import math
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from abjad.tools.datastructuretools.TypedList import TypedList


class TimespanInventory(TypedList):
    r'''A timespan inventory.

    ..  container:: example

        **Example 1:**

        ::

            >>> timespan_inventory_1 = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10),
            ...     ])

        ::

            >>> print format(timespan_inventory_1)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(3, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(6, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(10, 1),
                    ),
                ])

    ..  container:: example

        **Example 2:**

        ::

            >>> timespan_inventory_2 = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(15, 20),
            ...     ])

        ::

            >>> print format(timespan_inventory_2)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(6, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(15, 1),
                    stop_offset=durationtools.Offset(20, 1),
                    ),
                ])

    ..  container:: example

        **Example 3.** Empty timespan inventory:

        ::

            >>> timespan_inventory_3 = timespantools.TimespanInventory()

        ::

            >>> print format(timespan_inventory_3)
            timespantools.TimespanInventory([])

    Operations on timespan currently work in place.
    '''

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        r'''Keep material that intersects `timespan`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 16),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 8),
            ...     ])

        ::

            >>> timespan = timespantools.Timespan(5, 10)
            >>> result = timespan_inventory & timespan

        ::

            >>> print format(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(8, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1),
                    ),
                ])

        Operates in place and returns timespan inventory.
        '''
        new_timespans = []
        for current_timespan in self[:]:
            result = current_timespan & timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    def __sub__(self, timespan):
        r'''Delete material that intersects `timespan`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 16),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 8),
            ...     ])

        ::

            >>> timespan = timespantools.Timespan(5, 10)
            >>> result = timespan_inventory - timespan

        ::

            >>> print format(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(5, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(5, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(12, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(16, 1),
                    ),
                ])

        Operates in place and returns timespan inventory.
        '''
        new_timespans = []
        for current_timespan in self[:]:
            result = current_timespan - timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    ### PRIVATE METHODS ###

    def _get_offsets(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return expr.start_offset, expr.stop_offset
        elif hasattr(expr, 'timespan'):
            return expr.timespan.offsets
        else:
            raise TypeError(expr)

    def _get_timespan(self, expr):
        from abjad.tools import timespantools
        start_offset, stop_offset = self._get_offsets(expr)
        return timespantools.Timespan(start_offset, stop_offset)

    ### PUBLIC PROPERTIES ###

    @property
    def all_are_contiguous(self):
        r'''True when all timespans are time-contiguous:

        ::

            >>> timespan_inventory_1.all_are_contiguous
            True

        False when timespans not time-contiguous:

        ::

            >>> timespan_inventory_2.all_are_contiguous
            False

        True when empty:

        ::

            >>> timespan_inventory_3.all_are_contiguous
            True

        Returns boolean.
        '''
        if len(self) <= 1:
            return True
        timespans = sorted(self[:])
        last_stop_offset = timespans[0].stop_offset
        for timespan in timespans[1:]:
            if timespan.start_offset != last_stop_offset:
                return False
            last_stop_offset = timespan.stop_offset
        return True

    @property
    def all_are_nonoverlapping(self):
        r'''True when all timespans are non-overlapping:

        ::

            >>> timespan_inventory_1.all_are_nonoverlapping
            True

        False when timespans are overlapping:

        ::

            >>> timespan_inventory_2.all_are_nonoverlapping
            False

        True when empty:

        ::

            >>> timespan_inventory_3.all_are_nonoverlapping
            True

        Returns boolean.
        '''
        if len(self) <= 1:
            return True
        timespans = sorted(self[:])
        last_stop_offset = timespans[0].stop_offset
        for timespan in timespans[1:]:
            if timespan.start_offset < last_stop_offset:
                return False
            if last_stop_offset < timespan.stop_offset:
                last_stop_offset = timespan.stop_offset
        return True

    @property
    def all_are_well_formed(self):
        r'''True when all timespans are well-formed:

        ::

            >>> timespan_inventory_1.all_are_well_formed
            True

        ::

            >>> timespan_inventory_2.all_are_well_formed
            True

        Also true when empty:

        ::

            >>> timespan_inventory_3.all_are_well_formed
            True

        Otherwise false.

        Returns boolean.
        '''
        return all(self._get_timespan(expr).is_well_formed for expr in self)

    @property
    def axis(self):
        r'''Arithmetic mean of start- and stop-offsets.

            >>> timespan_inventory_1.axis
            Offset(5, 1)

        ::

            >>> timespan_inventory_2.axis
            Offset(10, 1)

        None when empty:

        ::

            >>> timespan_inventory_3.axis is None
            True

        Returns offset or none.
        '''
        if self:
            return (self.start_offset + self.stop_offset) / 2

    @property
    def duration(self):
        r'''Time from start offset to stop offset:

        ::

            >>> timespan_inventory_1.duration
            Duration(10, 1)

        ::

            >>> timespan_inventory_2.duration
            Duration(20, 1)

        Zero when empty:

        ::

            >>> timespan_inventory_3.duration
            Duration(0, 1)

        Returns duration.
        '''
        if self.stop_offset is not Infinity and \
            self.start_offset is not NegativeInfinity:
            return self.stop_offset - self.start_offset
        else:
            return durationtools.Duration(0)

    @property
    def is_sorted(self):
        r'''True when timespans are in time order:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10),
            ...     ])

        ::

            >>> timespan_inventory.is_sorted
            True

        Otherwise false:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(6, 10),
            ...     timespantools.Timespan(3, 6),
            ...     ])

        ::

            >>> timespan_inventory.is_sorted
            False

        Returns boolean.
        '''
        if len(self) < 2:
            return True
        for left_timespan, right_timespan in \
            sequencetools.iterate_sequence_pairwise_strict(self):
            if right_timespan.start_offset < left_timespan.start_offset:
                return False
            if left_timespan.start_offset == right_timespan.start_offset:
                if right_timespan.stop_offset < left_timespan.stop_offset:
                    return False
        return True

    @property
    def start_offset(self):
        r'''Earliest start offset of any timespan:

        ::

            >>> timespan_inventory_1.start_offset
            Offset(0, 1)

        ::

            >>> timespan_inventory_2.start_offset
            Offset(0, 1)

        Negative infinity when empty:

        ::

            >>> timespan_inventory_3.start_offset
            NegativeInfinity

        Returns offset or none.
        '''
        if self:
            return min([self._get_timespan(expr).start_offset
                for expr in self])
        else:
            return NegativeInfinity

    @property
    def stop_offset(self):
        r'''Latest stop offset of any timespan:

        ::

            >>> timespan_inventory_1.stop_offset
            Offset(10, 1)

        ::

            >>> timespan_inventory_2.stop_offset
            Offset(20, 1)

        Infinity when empty:

        ::

            >>> timespan_inventory_3.stop_offset
            Infinity

        Returns offset or none.
        '''
        if self:
            return max([self._get_timespan(expr).stop_offset for expr in self])
        else:
            return Infinity

    @property
    def timespan(self):
        r'''Timespan inventory timespan:

        ::

            >>> timespan_inventory_1.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        ::

            >>> timespan_inventory_2.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(20, 1))

        ::

            >>> timespan_inventory_3.timespan
            Timespan(start_offset=NegativeInfinity, stop_offset=Infinity)

        Returns timespan.
        '''
        from abjad.tools import timespantools
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    def compute_logical_and(self):
        r'''Compute logical AND of timespans.

        ..  container:: example

            **Example 1:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_and()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_and()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 3:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_and()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(8, 1),
                        ),
                    ])

        Same as setwise intersection.

        Operates in place and returns timespan inventory.
        '''
        if 1 < len(self):
            result = self[0]
            for timespan in self:
                if not timespan.intersects_timespan(result):
                    self[:] = []
                    return self
                else:
                    inventory = result & timespan
                    result = inventory[0]
            self[:] = [result]
        return self

    def compute_logical_or(self):
        r'''Compute logical OR of timespans.

        ..  container:: example

            **Example 1:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory()

            ::

                >>> result = timespan_inventory.compute_logical_or()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([])

        ..  container:: example

            **Example 2:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_or()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 3:**

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_or()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(12, 1),
                        ),
                    ])

        ..  container:: example

            **Example 4:**

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 2),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_or()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-2, 1),
                        stop_offset=durationtools.Offset(12, 1),
                        ),
                    ])

        ..  container:: example

            **Example 5:**

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(-2, 2),
                ...     timespantools.Timespan(10, 20),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_or()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-2, 1),
                        stop_offset=durationtools.Offset(2, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(10, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    ])

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        if self:
            timespans = [self[0]]
            for timespan in self[1:]:
                if timespans[-1]._can_fuse(timespan):
                    inventory = timespans[-1] | timespan
                    timespans[-1:] = inventory[:]
                else:
                    timespans.append(timespan)
        self[:] = timespans
        return self

    def compute_logical_xor(self):
        r'''Compute logical XOR of timespans.

        ..  container:: example

            **Example 1:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory()

            ::

                >>> result = timespan_inventory.compute_logical_xor()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([])

        ..  container:: example

            **Example 2:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_xor()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 3:**

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_xor()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(5, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(10, 1),
                        stop_offset=durationtools.Offset(12, 1),
                        ),
                    ])

        ..  container:: example

            **Example 4:**

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 2),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_xor()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-2, 1),
                        stop_offset=durationtools.Offset(0, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(2, 1),
                        stop_offset=durationtools.Offset(5, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(10, 1),
                        stop_offset=durationtools.Offset(12, 1),
                        ),
                    ])

        ..  container:: example

            **Example 5:**

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(-2, 2),
                ...     timespantools.Timespan(10, 20),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_xor()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-2, 1),
                        stop_offset=durationtools.Offset(2, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(10, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    ])

        ..  container:: example

            **Example 6:**

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(4, 8),
                ...     timespantools.Timespan(2, 6),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_xor()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(2, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(8, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 7:**

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(0, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.compute_logical_xor()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([])

        Operates in place and returns timespan inventory.
        '''
        all_fragments = []
        for i, timespan_1 in enumerate(self):
            timespan_1_fragments = [timespan_1]
            for j, timespan_2 in enumerate(self):
                if i == j:
                    continue
                revised_timespan_1_fragments = []
                for timespan_1_fragment in timespan_1_fragments:
                    if timespan_2.intersects_timespan(timespan_1_fragment):
                        result = timespan_1_fragment - timespan_2
                        revised_timespan_1_fragments.extend(result)
                    else:
                        revised_timespan_1_fragments.append(
                            timespan_1_fragment)
                timespan_1_fragments = revised_timespan_1_fragments
            all_fragments.extend(timespan_1_fragments)
        self[:] = all_fragments
        self.sort()
        return self

    def compute_overlap_factor(self, timespan=None):
        r'''Compute overlap factor of timespans:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(5, 15),
            ...     timespantools.Timespan(20, 25),
            ...     timespantools.Timespan(20, 30),
            ...     ])

        ..  container:: example

            **Example 1.** Compute overlap factor across the entire inventory:

            ::

                >>> timespan_inventory.compute_overlap_factor()
                Multiplier(7, 6)

        ..  container:: example

            **Example 2a.** Compute overlap factor within a specific timespan:

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(-15, 0))
                Multiplier(0, 1)

        ..  container:: example

            **Example 2b:**

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(-10, 5))
                Multiplier(1, 3)

        ..  container:: example

            **Example 2c:**

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(-5, 10))
                Multiplier(1, 1)

        ..  container:: example

            **Example 2d:**

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(0, 15))
                Multiplier(4, 3)

        ..  container:: example

            **Example 2e:**

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(5, 20))
                Multiplier(1, 1)

        ..  container:: example

            **Example 2f:**

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(10, 25))
                Multiplier(1, 1)

        ..  container:: example

            **Example 2g:**

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(15, 30))
                Multiplier(1, 1)

        Returns multiplier.
        '''
        from abjad.tools import timespantools
        if timespan is None:
            timespan = self.timespan
        time_relation = timerelationtools.timespan_2_intersects_timespan_1(
            timespan_1=timespan)
        timespan_inventory = self.get_timespans_that_satisfy_time_relation(
            time_relation)
        total_overlap = durationtools.Duration(sum(
            x.get_overlap_with_timespan(timespan) for x in timespan_inventory))
        overlap_factor = total_overlap / timespan.duration
        return overlap_factor

    def compute_overlap_factor_mapping(self):
        r'''Compute overlap factor for each consecutive offset pair in
        timespans:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(5, 15),
            ...     timespantools.Timespan(20, 25),
            ...     timespantools.Timespan(20, 30),
            ...     ])

        ::

            >>> mapping = timespan_inventory.compute_overlap_factor_mapping()
            >>> for timespan, overlap_factor in mapping.iteritems():
            ...     timespan.start_offset, timespan.stop_offset, overlap_factor
            ...
            (Offset(0, 1), Offset(5, 1), Multiplier(1, 1))
            (Offset(5, 1), Offset(10, 1), Multiplier(2, 1))
            (Offset(10, 1), Offset(15, 1), Multiplier(1, 1))
            (Offset(15, 1), Offset(20, 1), Multiplier(0, 1))
            (Offset(20, 1), Offset(25, 1), Multiplier(2, 1))
            (Offset(25, 1), Offset(30, 1), Multiplier(1, 1))

        Returns mapping.
        '''
        from abjad.tools import timespantools
        mapping = collections.OrderedDict()
        for start_offset, stop_offset in \
            sequencetools.iterate_sequence_pairwise_strict(sorted(
                self.count_offsets())):
            timespan = timespantools.Timespan(start_offset, stop_offset)
            overlap_factor = self.compute_overlap_factor(timespan=timespan)
            mapping[timespan] = overlap_factor
        return mapping

    def count_offsets(self):
        r'''Count offsets in inventory:

        ..  container:: example

            **Example 1:**

            ::

                >>> print format(timespan_inventory_1)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

            ::

                >>> for offset, count in sorted(
                ...     timespan_inventory_1.count_offsets().iteritems()):
                ...     offset, count
                ...
                (Offset(0, 1), 1)
                (Offset(3, 1), 2)
                (Offset(6, 1), 2)
                (Offset(10, 1), 1)

        ..  container:: example

            **Example 2:**

            ::

                >>> print format(timespan_inventory_2)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    ])

            ::

                >>> for offset, count in sorted(
                ...     timespan_inventory_2.count_offsets().iteritems()):
                ...     offset, count
                ...
                (Offset(0, 1), 1)
                (Offset(3, 1), 1)
                (Offset(6, 1), 1)
                (Offset(10, 1), 1)
                (Offset(15, 1), 1)
                (Offset(20, 1), 1)

        ..  container:: example

            **Example 3:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(0, 6),
                ...     timespantools.Timespan(0, 9),
                ...     ])
                >>> for offset, count in sorted(
                ...     timespan_inventory.count_offsets().iteritems()):
                ...     offset, count
                ...
                (Offset(0, 1), 3)
                (Offset(3, 1), 1)
                (Offset(6, 1), 1)
                (Offset(9, 1), 1)

        Returns counter.
        '''
        counter = collections.Counter()
        for timespan in self:
            counter[timespan.start_offset] += 1
            counter[timespan.stop_offset] += 1
        return counter

    def explode(self, inventory_count=None):
        r'''Explode timespans into inventories, avoiding overlap, and
        distributing density as evenly as possible.

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(5, 13),
            ...     timespantools.Timespan(6, 10),
            ...     timespantools.Timespan(8, 9),
            ...     timespantools.Timespan(15, 23),
            ...     timespantools.Timespan(16, 21),
            ...     timespantools.Timespan(17, 19),
            ...     timespantools.Timespan(19, 20),
            ...     timespantools.Timespan(25, 30),
            ...     timespantools.Timespan(26, 29),
            ...     timespantools.Timespan(32, 34),
            ...     timespantools.Timespan(34, 37),
            ...     ])

        ..  container:: example

            **Example 1.** Explode timespans into the optimal number of
            non-overlapping inventories:

            ::

                >>> for exploded_inventory in timespan_inventory.explode():
                ...     print format(exploded_inventory)
                ...
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(13, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(17, 1),
                        stop_offset=durationtools.Offset(19, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(19, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(34, 1),
                        stop_offset=durationtools.Offset(37, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(16, 1),
                        stop_offset=durationtools.Offset(21, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(25, 1),
                        stop_offset=durationtools.Offset(30, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(8, 1),
                        stop_offset=durationtools.Offset(9, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(23, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(26, 1),
                        stop_offset=durationtools.Offset(29, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(32, 1),
                        stop_offset=durationtools.Offset(34, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2.** Explode timespans into a less-than-optimal number of
            overlapping inventories:

            ::

                >>> for exploded_inventory in timespan_inventory.explode(
                ...     inventory_count=2):
                ...     print format(exploded_inventory)
                ...
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(13, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(23, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(25, 1),
                        stop_offset=durationtools.Offset(30, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(34, 1),
                        stop_offset=durationtools.Offset(37, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(8, 1),
                        stop_offset=durationtools.Offset(9, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(16, 1),
                        stop_offset=durationtools.Offset(21, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(17, 1),
                        stop_offset=durationtools.Offset(19, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(19, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(26, 1),
                        stop_offset=durationtools.Offset(29, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(32, 1),
                        stop_offset=durationtools.Offset(34, 1),
                        ),
                    ])

        ..  container:: example

            **Example 3.** Explode timespans into a greater-than-optimal number
            of non-overlapping inventories:

            ::

                >>> for exploded_inventory in timespan_inventory.explode(
                ...     inventory_count=6):
                ...     print format(exploded_inventory)
                ...
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(16, 1),
                        stop_offset=durationtools.Offset(21, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(34, 1),
                        stop_offset=durationtools.Offset(37, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(23, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(8, 1),
                        stop_offset=durationtools.Offset(9, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(17, 1),
                        stop_offset=durationtools.Offset(19, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(19, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(26, 1),
                        stop_offset=durationtools.Offset(29, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(32, 1),
                        stop_offset=durationtools.Offset(34, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(13, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(25, 1),
                        stop_offset=durationtools.Offset(30, 1),
                        ),
                    ])

        Returns inventories.
        '''
        assert isinstance(inventory_count, (type(None), int))
        if isinstance(inventory_count, int):
            assert 0 < inventory_count
        bounding_timespan = self.timespan
        global_overlap_factors = []
        empty_inventory_pairs = []
        result_inventories = []
        if inventory_count is not None:
            for i in range(inventory_count):
                global_overlap_factors.append(0)
                result_inventory = type(self)([])
                empty_inventory_pairs.append((i, result_inventory))
                result_inventories.append(result_inventory)
        for current_timespan in self:
            current_overlap_factor = \
                current_timespan.duration / bounding_timespan.duration
            if empty_inventory_pairs:
                i, empty_inventory = empty_inventory_pairs.pop()
                empty_inventory.append(current_timespan)
                global_overlap_factors[i] = current_overlap_factor
                continue
            nonoverlapping_inventories = []
            overlapping_inventories = []
            for i, result_inventory in enumerate(result_inventories):
                local_overlap_factor = result_inventory.compute_overlap_factor(
                    current_timespan)
                global_overlap_factor = global_overlap_factors[i]
                if not local_overlap_factor:
                    nonoverlapping_inventories.append(
                        (i, global_overlap_factor))
                else:
                    overlapping_inventories.append(
                        (i, local_overlap_factor, global_overlap_factor))
            nonoverlapping_inventories.sort(key=lambda x: x[1])
            overlapping_inventories.sort(key=lambda x: (x[1], x[2]))
            if not nonoverlapping_inventories and inventory_count is None:
                result_inventory = type(self)([current_timespan])
                global_overlap_factors.append(current_overlap_factor)
                result_inventories.append(result_inventory)
                continue
            if nonoverlapping_inventories:
                i = nonoverlapping_inventories[0][0]
            else:
                i = overlapping_inventories[0][0]
            result_inventory = result_inventories[i]
            result_inventory.append(current_timespan)
            global_overlap_factors[i] += current_overlap_factor
        return tuple(result_inventories)

    def get_timespan_that_satisfies_time_relation(self, time_relation):
        r'''Get timespan that satisifies `time_relation`:

        ::

            >>> timespan_1 = timespantools.Timespan(2, 5)
            >>> time_relation = \
            ...     timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory_1.get_timespan_that_satisfies_time_relation(
            ...     time_relation)
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        Returns timespan when timespan inventory contains exactly one
        timespan that satisfies `time_relation`.

        Raises exception when timespan inventory contains no timespan
        that satisfies `time_relation`.

        Raises exception when timespan inventory contains more than one
        timespan that satisfies `time_relation`.
        '''
        timespans = self.get_timespans_that_satisfy_time_relation(
            time_relation)
        if len(timespans) == 1:
            return timespans[0]
        elif 1 < len(timespans):
            raise Exception('extra timespan error.')
        else:
            raise Exception('missing timespan error.')

    def get_timespans_that_satisfy_time_relation(self, time_relation):
        r'''Get timespans that satisfy `time_relation`:

        ::

            >>> timespan_1 = timespantools.Timespan(2, 8)
            >>> time_relation = \
            ...     timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> result = \
            ...     timespan_inventory_1.get_timespans_that_satisfy_time_relation(
            ...     time_relation)

        ::

            >>> print format(result)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(6, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(10, 1),
                    ),
                ])

        Returns new timespan inventory.
        '''
        from abjad.tools import timerelationtools
        result = []
        for timespan in self:
            if isinstance(
                time_relation,
                timerelationtools.TimespanTimespanTimeRelation):
                if time_relation(timespan_2=timespan):
                    result.append(timespan)
            elif isinstance(
                time_relation,
                timerelationtools.OffsetTimespanTimeRelation):
                if time_relation(timespan=timespan):
                    result.append(timespan)
            else:
                raise ValueError
        return type(self)(result)

    def has_timespan_that_satisfies_time_relation(self, time_relation):
        r'''True when timespan inventory has timespan that
        satisfies `time_relation`:

        ::

            >>> timespan_1 = timespantools.Timespan(2, 8)
            >>> time_relation = \
            ...     timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory_1.has_timespan_that_satisfies_time_relation(
            ...     time_relation)
            True

        Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(10, 20)
            >>> time_relation = \
            ...     timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory_1.has_timespan_that_satisfies_time_relation(
            ...     time_relation)
            False

        Returns boolean.
        '''
        return bool(
            self.get_timespans_that_satisfy_time_relation(time_relation))

    def partition(self, include_tangent_timespans=False):
        r'''Partition timespans into inventories:

        ..  container:: example

            **Example 1:**

            ::

                >>> print format(timespan_inventory_1)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

            ::

                >>> for inventory in timespan_inventory_1.partition():
                ...     print format(inventory)
                ...
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2:**

            ::

                >>> print format(timespan_inventory_2)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    ])

            ::

                >>> for inventory in timespan_inventory_2.partition():
                ...     print format(inventory)
                ...
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    ])

        ..  container:: example

            **Example 3.** Treat tangent timespans as part of the same group with
            include_tangent_timespans:

            ::

                >>> for inventory in timespan_inventory_1.partition(
                ...     include_tangent_timespans=True):
                ...     print format(inventory)
                ...
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        Returns 0 or more inventories.
        '''
        if not self:
            return []
        inventories = []
        timespans = sorted(self[:])
        current_inventory = type(self)([timespans[0]])
        latest_stop_offset = current_inventory[0].stop_offset
        for current_timespan in timespans[1:]:
            if current_timespan.start_offset < latest_stop_offset:
                current_inventory.append(current_timespan)
            elif include_tangent_timespans and \
                current_timespan.start_offset == latest_stop_offset:
                current_inventory.append(current_timespan)
            else:
                inventories.append(current_inventory)
                current_inventory = type(self)([current_timespan])
            if latest_stop_offset < current_timespan.stop_offset:
                latest_stop_offset = current_timespan.stop_offset
        if current_inventory:
            inventories.append(current_inventory)
        return tuple(inventories)

    def reflect(self, axis=None):
        r'''Reflect timespans.

        ..  container:: example

            **Example 1.** Reflect timespans about timespan inventory axis:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.reflect()

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(4, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(4, 1),
                        stop_offset=durationtools.Offset(7, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(7, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2.** Reflect timespans about arbitrary axis:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.reflect(axis=Offset(15))

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(20, 1),
                        stop_offset=durationtools.Offset(24, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(24, 1),
                        stop_offset=durationtools.Offset(27, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(27, 1),
                        stop_offset=durationtools.Offset(30, 1),
                        ),
                    ])

        Operates in place and returns timespan inventory.
        '''
        if axis is None:
            axis = self.axis
        timespans = []
        for timespan in self:
            timespan = timespan.reflect(axis=axis)
            timespans.append(timespan)
        timespans.reverse()
        self[:] = timespans
        return self

    def remove_degenerate_timespans(self):
        r'''Remove degenerate timespans:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(5, 5),
            ...     timespantools.Timespan(5, 10),
            ...     timespantools.Timespan(5, 25),
            ...     ])

        ::

            >>> result = timespan_inventory.remove_degenerate_timespans()

        ::

            >>> print format(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(25, 1),
                    ),
                ])

        Operates in place and returns timespan inventory.
        '''
        timespans = [x for x in self if x.is_well_formed]
        self[:] = timespans
        return self

    def repeat_to_stop_offset(self, stop_offset):
        r'''Repeat timespans to `stop_offset`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10),
            ...     ])

        ::

            >>> result = timespan_inventory.repeat_to_stop_offset(15)

        ::

            >>> print format(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(3, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(6, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(10, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(13, 1),
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(13, 1),
                    stop_offset=durationtools.Offset(15, 1),
                    ),
                ])

        Operates in place and returns timespan inventory.
        '''
        assert self.is_sorted
        stop_offset = durationtools.Offset(stop_offset)
        assert self.stop_offset <= stop_offset
        current_timespan_index = 0
        if self:
            while self.stop_offset < stop_offset:
                current_timespan = self[current_timespan_index]
                translation = self.stop_offset - current_timespan.start_offset
                new_timespan = current_timespan.translate(translation)
                self.append(new_timespan)
                current_timespan_index += 1
            if stop_offset < self.stop_offset:
                self[-1] = self[-1].set_offsets(stop_offset=stop_offset)
        return self

    def rotate(self, count):
        r'''Rotate by `count` contiguous timespans.

        ..  container:: example

            **Example 1.** Rotate by one timespan to the left:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 4),
                ...     timespantools.Timespan(4, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.rotate(-1)

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(1, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(1, 1),
                        stop_offset=durationtools.Offset(7, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(7, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2.** Rotate by one timespan to the right:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 4),
                ...     timespantools.Timespan(4, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.rotate(1)

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(9, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(9, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        Operates in place and returns timespan inventory.
        '''
        assert isinstance(count, int)
        assert self.all_are_contiguous
        elements_to_move = count % len(self)
        if elements_to_move == 0:
            return
        left_timespans = self[:-elements_to_move]
        right_timespans = self[-elements_to_move:]
        split_offset = right_timespans[0].start_offset
        translation_to_left = split_offset - self.start_offset
        translation_to_left *= -1
        translation_to_right = self.stop_offset - split_offset
        translated_right_timespans = []
        for right_timespan in right_timespans:
            translated_right_timespan = right_timespan.translate_offsets(
                translation_to_left, translation_to_left)
            translated_right_timespans.append(translated_right_timespan)
        translated_left_timespans = []
        for left_timespan in left_timespans:
            translated_left_timespan = left_timespan.translate_offsets(
                translation_to_right, translation_to_right)
            translated_left_timespans.append(translated_left_timespan)
        new_timespans = translated_right_timespans + translated_left_timespans
        self[:] = new_timespans
        return self

    def round_offsets(self, multiplier, anchor=Left, must_be_well_formed=True):
        '''Round offsets of timespans in inventory to multiples of
        `multiplier`:

        ..  container:: example

            **Example 1:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 2),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> rounded_inventory = timespan_inventory.round_offsets(3)
                >>> print format(rounded_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(9, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 2),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> rounded_inventory = timespan_inventory.round_offsets(5)
                >>> print format(rounded_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(5, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 3:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 2),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> rounded_inventory = timespan_inventory.round_offsets(
                ...     5,
                ...     anchor=Right,
                ...     )
                >>> print format(rounded_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-5, 1),
                        stop_offset=durationtools.Offset(0, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(5, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 4:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 2),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> rounded_inventory = timespan_inventory.round_offsets(
                ...     5,
                ...     anchor=Right,
                ...     must_be_well_formed=False,
                ...     )
                >>> print format(rounded_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(0, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(5, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        for timespan in self:
            timespan = timespan.round_offsets(
                multiplier,
                anchor=anchor,
                must_be_well_formed=must_be_well_formed,
                )
            timespans.append(timespan)
        self[:] = timespans
        return self

    def scale(self, multiplier, anchor=Left):
        r'''Scale timespan by `multiplier` relative to `anchor`.

        ..  container:: example

            **Example 1.** Scale timespans relative to timespan inventory start offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.scale(2)

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(9, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(14, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2.** Scale timespans relative to timespan inventory stop offset:

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.scale(2, anchor=Right)

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-3, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(2, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        for timespan in self:
            timespan = timespan.scale(multiplier, anchor=anchor)
            timespans.append(timespan)
        self[:] = timespans
        return self

    def split_at_offset(self, offset):
        '''Split timespans at `offset`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10),
            ...     ])

        ..  container:: example

            **Example 1:**

            ::

                >>> left, right = timespan_inventory.split_at_offset(4)

            ::

                >>> print format(left)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(4, 1),
                        ),
                    ])

            ::

                >>> print format(right)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(4, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2:**

            ::

                >>> left, right = timespan_inventory.split_at_offset(6)

            ::

                >>> print format(left)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    ])

            ::

                >>> print format(right)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        ..  container:: example

            **Example 3:**

            ::

                >>> left, right = timespan_inventory.split_at_offset(-1)

            ::

                >>> print format(left)
                timespantools.TimespanInventory([])

            ::

                >>> print format(right)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])

        Returns inventories.
        '''
        offset = durationtools.Offset(offset)
        during_time_relation = timerelationtools.OffsetTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                'timespan.start < offset',
                'offset < timespan.stop'],
                logical_operator='and',
                ),
            offset=offset,
            )
        during_timespans = self.get_timespans_that_satisfy_time_relation(
            during_time_relation)
        before_time_relation = timerelationtools.OffsetTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                'timespan.stop <= offset'],
                ),
            offset=offset,
            )
        before_timespans = self.get_timespans_that_satisfy_time_relation(
            before_time_relation)
        after_time_relation = timerelationtools.OffsetTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                'offset <= timespan.start'],
                ),
            offset=offset,
            )
        after_timespans = self.get_timespans_that_satisfy_time_relation(
            after_time_relation)
        before_inventory = type(self)(before_timespans)
        after_inventory = type(self)(after_timespans)
        for timespan in during_timespans:
            before_timespan, after_timespan = timespan.split_at_offset(offset)
            before_inventory.append(before_timespan)
            after_inventory.append(after_timespan)
        before_inventory.sort()
        after_inventory.sort()
        return before_inventory, after_inventory

    def split_at_offsets(self, offsets):
        '''Split timespans at `offsets`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(4, 10),
            ...     timespantools.Timespan(15, 20),
            ...     ])

        ::

            >>> offsets = [-1, 3, 6, 12, 13]

        ..  container:: example

            **Example 1:**

            ::

                >>> for inventory in timespan_inventory.split_at_offsets(offsets):
                ...     print format(inventory)
                ...
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(4, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ])
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2:**

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([])
                >>> timespan_inventory.split_at_offsets(offsets)
                [TimespanInventory([])]

        Returns 1 or more inventories.
        '''
        inventories = [self]
        if not self:
            return inventories
        offsets = sorted(set(durationtools.Offset(x) for x in offsets))
        offsets = [x for x in offsets
            if self.start_offset < x < self.stop_offset]
        for offset in offsets:
            shards = [x for x in inventories[-1].split_at_offset(offset)
                if x]
            if shards:
                inventories[-1:] = shards
        return inventories

    def stretch(self, multiplier, anchor=None):
        r'''Stretch timespans by `multiplier` relative to `anchor`.

        ..  container:: example

            **Example 1:** Stretch timespans relative to timespan inventory
            start offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.stretch(2)

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(12, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(12, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2:** Stretch timespans relative to arbitrary anchor:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])


            ::

                >>> result = timespan_inventory.stretch(2, anchor=Offset(8))

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-8, 1),
                        stop_offset=durationtools.Offset(-2, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-2, 1),
                        stop_offset=durationtools.Offset(4, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(4, 1),
                        stop_offset=durationtools.Offset(12, 1),
                        ),
                    ])

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        if anchor is None:
            anchor = self.start_offset
        for timespan in self:
            timespan = timespan.stretch(multiplier, anchor)
            timespans.append(timespan)
        self[:] = timespans
        return self

    def translate(self, translation=None):
        r'''Translate timespans by `translation`.

        ..  container:: example

            **Example 1.** Translate timespan by offset ``50``:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.translate(50)

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(50, 1),
                        stop_offset=durationtools.Offset(53, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(53, 1),
                        stop_offset=durationtools.Offset(56, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(56, 1),
                        stop_offset=durationtools.Offset(60, 1),
                        ),
                    ])

        Operates in place and returns timespan inventory.
        '''
        return self.translate_offsets(translation, translation)

    def translate_offsets(
        self,
        start_offset_translation=None,
        stop_offset_translation=None,
        ):
        r'''Translate timespans by `start_offset_translation`
        and `stop_offset_translation`.

        ..  container:: example

            **Example 1.** Translate timespan start- and stop-offsets equally:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.translate_offsets(50, 50)

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(50, 1),
                        stop_offset=durationtools.Offset(53, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(53, 1),
                        stop_offset=durationtools.Offset(56, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(56, 1),
                        stop_offset=durationtools.Offset(60, 1),
                        ),
                    ])

        ..  container:: example

            **Example 2.** Translate timespan stop-offsets only:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])

            ::

                >>> result = timespan_inventory.translate_offsets(
                ...     stop_offset_translation=20)

            ::

                >>> print format(timespan_inventory)
                timespantools.TimespanInventory([
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(23, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(26, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(30, 1),
                        ),
                    ])

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        for timespan in self:
            timespan = timespan.translate_offsets(
                start_offset_translation,
                stop_offset_translation,
                )
            timespans.append(timespan)
        self[:] = timespans
        return self
