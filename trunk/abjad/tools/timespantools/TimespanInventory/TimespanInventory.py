import copy
import math
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class TimespanInventory(ObjectInventory):
    r'''Timespan inventory.

    Example 1::

        >>> timespan_inventory_1 = timespantools.TimespanInventory([
        ...     timespantools.Timespan(0, 3),
        ...     timespantools.Timespan(3, 6),
        ...     timespantools.Timespan(6, 10)])

    ::

        >>> z(timespan_inventory_1)
        timespantools.TimespanInventory([
            timespantools.Timespan(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(3, 1)
                ),
            timespantools.Timespan(
                start_offset=durationtools.Offset(3, 1),
                stop_offset=durationtools.Offset(6, 1)
                ),
            timespantools.Timespan(
                start_offset=durationtools.Offset(6, 1),
                stop_offset=durationtools.Offset(10, 1)
                )
            ])

    Example 2::

        >>> timespan_inventory_2 = timespantools.TimespanInventory([
        ...     timespantools.Timespan(0, 10),
        ...     timespantools.Timespan(3, 6),
        ...     timespantools.Timespan(15, 20)])

    ::

        >>> z(timespan_inventory_2)
        timespantools.TimespanInventory([
            timespantools.Timespan(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(10, 1)
                ),
            timespantools.Timespan(
                start_offset=durationtools.Offset(3, 1),
                stop_offset=durationtools.Offset(6, 1)
                ),
            timespantools.Timespan(
                start_offset=durationtools.Offset(15, 1),
                stop_offset=durationtools.Offset(20, 1)
                )
            ])

    Example 3. Empty timespan inventory:

    ::

        >>> timespan_inventory_3 = timespantools.TimespanInventory()

    ::

        >>> z(timespan_inventory_3)
        timespantools.TimespanInventory([])

    Operations on timespan currently work in place.
    '''

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Keep material that intersects `timespan`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 16),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 8)])

        ::

            >>> timespan = timespantools.Timespan(5, 10)
            >>> result = timespan_inventory & timespan

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(8, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        new_timespans = []
        for current_timespan in self[:]:
            result = current_timespan & timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    def __sub__(self, timespan):
        '''Delete material that intersects `timespan`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 16),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 8)])

        ::

            >>> timespan = timespantools.Timespan(5, 10)
            >>> result = timespan_inventory - timespan

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(5, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(5, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(16, 1)
                    )
                ])

        Operate in place and return timespan inventory.
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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def all_are_contiguous(self):
        '''True when all timespans are time-contiguous::

            >>> timespan_inventory_1.all_are_contiguous
            True

        False when timespans not time-contiguous::

            >>> timespan_inventory_2.all_are_contiguous
            False

        True when empty::

            >>> timespan_inventory_3.all_are_contiguous
            True

        Return boolean.
        '''
        if len(self) <= 1:
            return True
        last_stop_offset = self[0].stop_offset
        for timespan in self[1:]:
            if timespan.start_offset != last_stop_offset:
                return False
            last_stop_offset = timespan.stop_offset
        return True

    @property
    def all_are_well_formed(self):
        '''True when all timespans are well-formed::

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

        Return boolean.
        '''
        return all([self._get_timespan(expr).is_well_formed for expr in self])

    @property
    def axis(self):
        '''Arithmetic mean of start- and stop-offsets.

            >>> timespan_inventory_1.axis
            Offset(5, 1)

        ::

            >>> timespan_inventory_2.axis
            Offset(10, 1)

        None when empty:

        ::

            >>> timespan_inventory_3.axis is None
            True

        Return offset or none.
        '''
        if self:
            return (self.start_offset + self.stop_offset) / 2

    @property
    def duration(self):
        '''Time from start offset to stop offset::

            >>> timespan_inventory_1.duration
            Duration(10, 1)

        ::

            >>> timespan_inventory_2.duration
            Duration(20, 1)

        Zero when empty:

        ::

            >>> timespan_inventory_3.duration
            Duration(0, 1)

        Return duration.
        '''
        if self.stop_offset is not Infinity and self.start_offset is not NegativeInfinity:
            return self.stop_offset - self.start_offset
        else:
            return durationtools.Duration(0)

    @property
    def is_sorted(self):
        '''True when timespans are in time order:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> timespan_inventory.is_sorted
            True

        Otherwise false:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(6, 10),
            ...     timespantools.Timespan(3, 6)])

        ::

            >>> timespan_inventory.is_sorted
            False
    
        Return boolean.
        '''
        if len(self) < 2:
            return True
        for left_timespan, right_timespan in sequencetools.iterate_sequence_pairwise_strict(self):
            if right_timespan.start_offset < left_timespan.start_offset:
                return False
            if left_timespan.start_offset == right_timespan.start_offset:
                if right_timespan.stop_offset < left_timespan.stop_offset:
                    return False
        return True

    @property
    def start_offset(self):
        '''Earliest start offset of any timespan:

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
            
        Return offset or none.
        '''
        if self:
            return min([self._get_timespan(expr).start_offset for expr in self])
        else:
            return NegativeInfinity

    @property
    def stop_offset(self):
        '''Latest stop offset of any timespan:

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

        Return offset or none.
        '''
        if self:
            return max([self._get_timespan(expr).stop_offset for expr in self])
        else:
            return Infinity

    @property
    def timespan(self):
        '''Timespan inventory timespan:

        ::

            >>> timespan_inventory_1.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        ::

            >>> timespan_inventory_2.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(20, 1))

        ::

            >>> timespan_inventory_3.timespan
            Timespan()

        Return timespan.
        '''
        from abjad.tools import timespantools
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    def compute_logical_and(self):
        '''Compute logical AND of timespans.

        Example 1:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10)])

        ::

            >>> result = timespan_inventory.compute_logical_and()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Example 2:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(5, 12)])

        ::

            >>> result = timespan_inventory.compute_logical_and()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Example 3:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 8)])

        ::

            >>> result = timespan_inventory.compute_logical_and()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(8, 1)
                    )
                ])

        Same as setwise intersection.

        Operate in place and return timespan inventory.
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
        '''Compute logical OR of timespans.

        Example 1:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory()

        ::

            >>> result = timespan_inventory.compute_logical_or()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([])

        Example 2:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10)])

        ::

            >>> result = timespan_inventory.compute_logical_or()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Example 3:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(5, 12)])

        ::

            >>> result = timespan_inventory.compute_logical_or()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    )
                ])

        Example 4:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 2)])

        ::

            >>> result = timespan_inventory.compute_logical_or()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    )
                ])

        Example 5:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(-2, 2),
            ...     timespantools.Timespan(10, 20)])

        ::

            >>> result = timespan_inventory.compute_logical_or()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                ])

        Operate in place and return timespan inventory.
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
        '''Compute logical XOR of timespans.

        Example 1:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory()

        ::

            >>> result = timespan_inventory.compute_logical_xor()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([])

        Example 2:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10)])

        ::

            >>> result = timespan_inventory.compute_logical_xor()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Example 3:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(5, 12)])

        ::

            >>> result = timespan_inventory.compute_logical_xor()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(5, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    )
                ])

        Example 4:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 2)])

        ::

            >>> result = timespan_inventory.compute_logical_xor()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(0, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(2, 1),
                    stop_offset=durationtools.Offset(5, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    )
                ])

        Example 5:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(-2, 2),
            ...     timespantools.Timespan(10, 20)])

        ::

            >>> result = timespan_inventory.compute_logical_xor()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                ])

        Example 6:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(4, 8),
            ...     timespantools.Timespan(2, 6)])

        ::

            >>> result = timespan_inventory.compute_logical_xor()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(8, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Example 7:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 10),
            ...     timespantools.Timespan(0, 10)])

        ::

            >>> result = timespan_inventory.compute_logical_xor()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([])

        Operate in place and return timespan inventory.
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
                        revised_timespan_1_fragments.append(timespan_1_fragment)
                timespan_1_fragments = revised_timespan_1_fragments
            all_fragments.extend(timespan_1_fragments)
        self[:] = all_fragments
        self.sort()
        return self

    def get_timespan_that_satisfies_time_relation(self, time_relation):
        r'''Get timespan that satisifies `time_relation`:

        ::

            >>> timespan_1 = timespantools.Timespan(2, 5)
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory_1.get_timespan_that_satisfies_time_relation(time_relation)
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        Return timespan when timespan inventory contains exactly one timespan
        that satisfies `time_relation`.

        Raise exception when timespan inventory contains no timespan
        that satisfies `time_relation`.

        Raise exception when timespan inventory contains more than one timespan
        that satisfies `time_relation`.
        '''
        timespans = self.get_timespans_that_satisfy_time_relation(time_relation)
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
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> result = timespan_inventory_1.get_timespans_that_satisfy_time_relation(
            ...     time_relation)

        ::

            >>> z(result)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(6, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Return new timespan inventory.
        '''
        from abjad.tools import timerelationtools
        result = []
        for timespan in self:
            if isinstance(time_relation, timerelationtools.TimespanTimespanTimeRelation):
                if time_relation(timespan_2=timespan):
                    result.append(timespan)
            elif isinstance(time_relation, timerelationtools.OffsetTimespanTimeRelation):
                if time_relation(timespan=timespan):
                    result.append(timespan)
            else:
                raise ValueError
        return type(self)(result)

    def has_timespan_that_satisfies_time_relation(self, time_relation):
        r'''True when timespan inventory has timespan that satisfies `time_relation`:

        ::

            >>> timespan_1 = timespantools.Timespan(2, 8)
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory_1.has_timespan_that_satisfies_time_relation(time_relation)
            True

        Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(10, 20)
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory_1.has_timespan_that_satisfies_time_relation(time_relation)
            False

        Return boolean.
        '''
        return bool(self.get_timespans_that_satisfy_time_relation(time_relation))

    def reflect(self, axis=None):
        '''Reflect timespans.

        Example 1. Reflect timespans about timespan inventory axis:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.reflect()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(4, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(4, 1),
                    stop_offset=durationtools.Offset(7, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(7, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Example 2. Reflect timespans about arbitrary axis:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.reflect(axis=Offset(15))

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(20, 1),
                    stop_offset=durationtools.Offset(24, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(24, 1),
                    stop_offset=durationtools.Offset(27, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(27, 1),
                    stop_offset=durationtools.Offset(30, 1)
                    )
                ])

        Operate in place and return timespan inventory.
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
        '''Remove degenerate timespans:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(5, 10),
            ...     timespantools.Timespan(5, 15),
            ...     timespantools.Timespan(5, 20)])

        ::

            >>> result = timespan_inventory.translate_offsets(stop_offset_translation=-10)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(0, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(5, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        ::

            >>> result = timespan_inventory.remove_degenerate_timespans()

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        timespans = [x for x in self if x.is_well_formed]
        self[:] = timespans
        return self

    def repeat_to_stop_offset(self, stop_offset):
        '''Repeat timespans to `stop_offset`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.repeat_to_stop_offset(15)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(3, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(6, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(13, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(13, 1),
                    stop_offset=durationtools.Offset(15, 1)
                    )
                ])

        Operate in place and return timespan inventory.
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
        '''Rotate by `count` contiguous timespans.

        Example 1. Rotate by one timespan to the left:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 4),
            ...     timespantools.Timespan(4, 10)])

        ::

            >>> result = timespan_inventory.rotate(-1)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(1, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(1, 1),
                    stop_offset=durationtools.Offset(7, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(7, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Example 2. Rotate by one timespan to the right:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 4),
            ...     timespantools.Timespan(4, 10)])

        ::

            >>> result = timespan_inventory.rotate(1)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(6, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(9, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(9, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Operate in place and return timespan inventory.
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

    def scale(self, multiplier, anchor=Left):
        '''Scale timespan by `multiplier` relative to `anchor`. 

        Example 1. Scale timespans relative to timespan inventory start offset:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.scale(2)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(6, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(9, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(14, 1)
                    )
                ])

        Example 2. Scale timespans relative to timespan inventory stop offset:

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.scale(2, anchor=Right)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-3, 1),
                    stop_offset=durationtools.Offset(3, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(6, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(2, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        timespans = []
        for timespan in self:
            timespan = timespan.scale(multiplier, anchor=anchor)
            timespans.append(timespan)
        self[:] = timespans
        return self

    def stretch(self, multiplier, anchor=None):
        '''Stretch timespans by `multiplier` relative to `anchor`.

        Example 1: Stretch timespans relative to timespan inventory start offset:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.stretch(2)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(6, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(12, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                ])

        Example 2: Stretch timespans relative to arbitrary anchor:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])


        ::

            >>> result = timespan_inventory.stretch(2, anchor=Offset(8))

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-8, 1),
                    stop_offset=durationtools.Offset(-2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(4, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(4, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    )
                ])

        Operate in place and return timespan inventory.
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
        '''Translate timespans by `translation`.

        Example 1. Translate timespan by offset ``50``:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.translate(50)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(50, 1),
                    stop_offset=durationtools.Offset(53, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(53, 1),
                    stop_offset=durationtools.Offset(56, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(56, 1),
                    stop_offset=durationtools.Offset(60, 1)
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        return self.translate_offsets(translation, translation)

    def translate_offsets(self, start_offset_translation=None, stop_offset_translation=None):
        '''Translate timespans by `start_offset_translation`
        and `stop_offset_translation`.

        Example 1. Translate timespan start- and stop-offsets equally::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.translate_offsets(50, 50)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(50, 1),
                    stop_offset=durationtools.Offset(53, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(53, 1),
                    stop_offset=durationtools.Offset(56, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(56, 1),
                    stop_offset=durationtools.Offset(60, 1)
                    )
                ])

        Example 2. Translate timespan stop-offsets only:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::

            >>> result = timespan_inventory.translate_offsets(stop_offset_translation=20)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(23, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(26, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(30, 1)
                    )
                ])

        Operate in place and return timespan inventory.
        '''
        timespans = []
        for timespan in self:
            timespan = timespan.translate_offsets(start_offset_translation, stop_offset_translation)
            timespans.append(timespan)
        self[:] = timespans
        return self
