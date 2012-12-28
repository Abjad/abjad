import copy
import math
from abjad.tools import durationtools
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class TimespanInventory(ObjectInventory):
    r'''.. versionadded:: 2.11

    Timespan inventory::

        >>> timespan_inventory = timespantools.TimespanInventory()

    ::

        >>> timespan_inventory.append(timespantools.Timespan(0, 3))
        >>> timespan_inventory.append(timespantools.Timespan(3, 6))
        >>> timespan_inventory.append(timespantools.Timespan(6, 10))

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
                )
            ])

    SymbolicTimespan inventory.
    '''

    ### PRIVATE METHODS ###

    def _set_start_offset(self, start_offset):
        from abjad.tools import timespantools
        start_offset = durationtools.Offset(start_offset)
        assert self.start_offset <= start_offset
        delete_timespan = timespantools.Timespan(self.start_offset, start_offset)
        self.delete_material_that_intersects_timespan(delete_timespan)

    def _set_stop_offset(self, stop_offset):
        from abjad.tools import timespantools
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset <= self.stop_offset
        delete_timespan = timespantools.Timespan(stop_offset, self.stop_offset)
        self.delete_material_that_intersects_timespan(delete_timespan)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def all_are_contiguous(self):
        '''True when all elements in inventory are time-contiguous.
        Also true when inventory is empty.
        Otherwise false.

        .. note:: add example.

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
    def axis(self):
        '''Arithmetic mean of inventory start- and stop-offsets.

        Return offset or none.
        '''
        if self:
            return (self.start_offset + self.stop_offset) / 2

    @property
    def contents_length(self):
        '''Sum of the length of all timespans in inventory.

        .. note:: add example.

        Return nonnegative integer.
        '''
        return sum([len(timespan) for timespan in self])
    
    @property
    def start_offset(self):
        '''Earliest start offset of any timespan in inventory.

        Return offset or none.
        '''
        if self:
            return min([timespan.start_offset for timespan in self])

    @property
    def stop_offset(self):
        '''Latest stop offset of any timespan in inventory.

        Return offset or none.
        '''
        if self:
            return max([timespan.stop_offset for timespan in self])

    ### PUBLIC METHODS ###

    def delete_material_that_intersects_timespan(self, timespan_2):
        from abjad.tools import timerelationtools
        for timespan_1 in self[:]:
            if timerelationtools.timespan_2_curtails_timespan_1(timespan_1, timespan_2):
                timespan_1.set_offsets(stop_offset=timespan_2.start_offset)
            elif timerelationtools.timespan_2_delays_timespan_1(timespan_1, timespan_2):
                timespan_1.set_offsets(start_offset=timespan_2.stop_offset)
            elif timerelationtools.timespan_2_contains_timespan_1_improperly(timespan_1, timespan_2):
                self.remove(timespan_1)

    def get_timespan_that_satisfies_time_relation(self, time_relation):
        r'''Get timespan that satisifies `time_relation`::

            >>> timespan_1 = timerelationtools.expr_to_timespan((2, 5))
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.get_timespan_that_satisfies_time_relation(time_relation)
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
        r'''Get timespans that satisfy `time_relation`::

            >>> timespan_1 = timerelationtools.expr_to_timespan((2, 8))
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespans = timespan_inventory.get_timespans_that_satisfy_time_relation(time_relation)

        ::

            >>> for timespan in timespans:
            ...     timespan
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))
            Timespan(start_offset=Offset(6, 1), stop_offset=Offset(10, 1))

        Return list of ``0`` or more timespans.
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
        return result

    def has_timespan_that_satisfies_time_relation(self, time_relation):
        r'''True when timespan inventory has timespan that satisfies `time_relation`::

            >>> timespan_1 = timerelationtools.expr_to_timespan((2, 8))
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.has_timespan_that_satisfies_time_relation(time_relation)
            True

        Otherwise false::

            >>> timespan_1 = timerelationtools.expr_to_timespan((10, 20))
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.has_timespan_that_satisfies_time_relation(time_relation)
            False

        Return boolean.
        '''
        return bool(self.get_timespans_that_satisfy_time_relation(time_relation))

    def keep_material_that_intersects_timespan(self, keep_timespan):
        from abjad.tools import timerelationtools
        for timespan_1 in self[:]:
            if timerelationtools.timespan_2_contains_timespan_1_improperly(timespan_1, keep_timespan):
                pass
            elif not timerelationtools.timespan_2_intersects_timespan_1(timespan_1, keep_timespan):
                self.remove(timespan_1)
            elif timerelationtools.timespan_2_delays_timespan_1(timespan_1, keep_timespan):
                timespan_1.set_offsets(stop_offset=keep_timespan.stop_offset)
            elif timerelationtools.timespan_2_curtails_timespan_1(timespan_1, keep_timespan):
                timespan_1.set_offsets(start_offset=keep_timespan.start_offset)
            elif timerelationtools.timespan_2_trisects_timespan_1(timespan_1, keep_timespan):
                timespan_1.set_offsets(start_offset=keep_timespan.start_offset)
                timespan_1.set_offsets(stop_offset=keep_timespan.stop_offset)
            else:
                raise ValueError

    def repeat_to_stop_offset(self, stop_offset):
        '''Copy timespans in inventory and repeat to `stop_offset`.

        .. note:: add example.

        Operate in place and return none.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert self.stop_offset <= stop_offset
        current_timespan_index = 0
        while self.stop_offset < stop_offset:
            new_timespan = copy.deepcopy(self[current_timespan_index])
            new_timespan._start_offset = self.stop_offset
            self.append(new_timespan)
            current_timespan_index += 1
        if stop_offset < self.stop_offset:
            self[-1].set_offsets(stop_offset=stop_offset)

    def reverse(self):
        '''Flip timespans about time axis.

        Also reverse timespans' contents.

        Operate in place and return none.
        '''
        axis = self.axis
        for timespan in self: 
            start_distance = timespan.start_offset - axis
            stop_distance = timespan.stop_offset - axis
            new_start_offset = axis - stop_distance
            new_stop_offset = axis - start_distance
            timespan._start_offset = new_start_offset
            timespan._stop_offset = new_stop_offset
            if hasattr(timespan, 'reverse'):
                timespan.reverse()

    def rotate(self, rotation):
        '''Rotate *elements* of timespans.

        .. note:: add example.
        
        Operation only makes sense if timespans are contiguous.

        Operate in place and return none.
        '''
        assert isinstance(rotation, int)
        assert self.all_are_contiguous
        elements_to_move = rotation % self.contents_length
        if elements_to_move == 0:
            return
        if True:
            for timespan in reversed(self[:]):
                if len(timespan) <= elements_to_move:
                    inventory_start_offset = self.start_offset
                    self.remove(timespan)
                    self.translate_timespans(timespan.duration)
                    timespan._start_offset = inventory_start_offset
                    self.insert(0, timespan)
                    elements_to_move -= len(timespan)
                elif elements_to_move < len(timespan):
                    left_timespan, right_timespan = timespan.fracture(-elements_to_move)
                    inventory_start_offset = self.start_offset
                    self.remove(timespan)
                    self.append(left_timespan)
                    self.translate_timespans(right_timespan.duration)
                    right_timespan._start_offset = inventory_start_offset
                    self.insert(0, right_timespan)
                    elements_to_move -= len(right_timespan)
                if elements_to_move < 0:
                    raise Exception(elements_to_move)
                if elements_to_move == 0:
                    break

    def set_offsets(self, start_offset=None, stop_offset=None):
        '''Operate in place and return none.
        '''
        if start_offset is not None:
            raise NotImplementedError
        stop_offset = durationtools.Offset(stop_offset)
        inventory_stop_offset = self.stop_offset
        if stop_offset < inventory_stop_offset:
            self._set_stop_offset(stop_offset)
        elif inventory_stop_offset < stop_offset:
            self.repeat_to_stop_offset(stop_offset)

    # TODO: change to 
    #  self.translate_all_timespan_offsets(start_offset_translation=None, stop_offset_translation=None)
    def translate_timespans(self, addendum):
        '''Translate every timespan in inventory by `addendum`.
        
        Operate in place and return none.
        '''
        for timespan in self:
            timespan._start_offset = durationtools.Offset(timespan.start_offset + addendum)
            timespan._stop_offset = durationtools.Offset(timespan.stop_offset + addendum)
