import copy
import math
from abjad.tools import durationtools
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class TimespanInventory(ObjectInventory):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    SymbolicTimespan inventory::

        >>> timespan_inventory = timetools.TimespanInventory()

    ::

        >>> timespan_inventory.append(durationtools.TimespanConstant(0, 3))
        >>> timespan_inventory.append(durationtools.TimespanConstant(3, 6))
        >>> timespan_inventory.append(durationtools.TimespanConstant(6, 10))

    ::

        >>> z(timespan_inventory)
        timetools.TimespanInventory([
            durationtools.TimespanConstant(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(3, 1)
                ),
            durationtools.TimespanConstant(
                start_offset=durationtools.Offset(3, 1),
                stop_offset=durationtools.Offset(6, 1)
                ),
            durationtools.TimespanConstant(
                start_offset=durationtools.Offset(6, 1),
                stop_offset=durationtools.Offset(10, 1)
                )
            ])

    SymbolicTimespan inventory.
    '''

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        ObjectInventory.__init__(self, *args, **kwargs)

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

    def adjust_to_stop_offset(self, stop_offset):
        '''Operate in place and return none.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        inventory_stop_offset = self.stop_offset
        if stop_offset < inventory_stop_offset:
            self.trim_to_stop_offset(stop_offset)
        elif inventory_stop_offset < stop_offset:
            self.repeat_to_stop_offset(stop_offset)

    def delete_material_that_intersects_timespan(self, timespan_2):
        from experimental import timetools
        for timespan_1 in self[:]:
            if timetools.timespan_2_curtails_timespan_1(timespan_1, timespan_2):
                timespan_1.trim_to_stop_offset(timespan_2.start_offset)
            elif timetools.timespan_2_delays_timespan_1(timespan_1, timespan_2):
                timespan_1.trim_to_start_offset(timespan_2.stop_offset)
            elif timetools.timespan_2_contains_timespan_1_improperly(timespan_1, timespan_2):
                self.remove(timespan_1)

    def get_timespan_that_satisfies_inequality(self, timespan_inequality):
        r'''Get timespan that satisifies `timespan_inequality`::

            >>> timespan_1 = timetools.expr_to_timespan((2, 5))
            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.get_timespan_that_satisfies_inequality(timespan_inequality)
            TimespanConstant(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        Return timespan when timespan inventory contains exactly one timespan
        that satisfies `timespan_inequality`.

        Raise exception when timespan inventory contains no timespan
        that satisfies `timespan_inequality`.

        Raise exception when timespan inventory contains more than one timespan
        that satisfies `timespan_inequality`.
        '''
        timespans = self.get_timespans_that_satisfy_inequality(timespan_inequality)
        if len(timespans) == 1:
            return timespans[0]
        elif 1 < len(timespans):
            raise Exception('extra timespan error.')
        else:
            raise Exception('missing timespan error.')

    def get_timespans_that_satisfy_inequality(self, timespan_inequality):
        r'''Get timespans that satisfy `timespan_inequality`::

            >>> timespan_1 = timetools.expr_to_timespan((2, 8))
            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespans = timespan_inventory.get_timespans_that_satisfy_inequality(timespan_inequality)

        ::

            >>> for timespan in timespans:
            ...     timespan
            TimespanConstant(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))
            TimespanConstant(start_offset=Offset(6, 1), stop_offset=Offset(10, 1))

        Return list of ``0`` or more timespans.
        '''
        from experimental import timetools
        result = []
        for timespan in self:
            if isinstance(timespan_inequality, timetools.TimespanInequality):
                if timespan_inequality(timespan_2=timespan):
                    result.append(timespan)
            elif isinstance(timespan_inequality, timetools.TimepointInequality):
                if timespan_inequality(timespan=timespan):
                    result.append(timespan)
            else:
                raise ValueError
        return result

    def has_timespan_that_satisfies_inequality(self, timespan_inequality):
        r'''True when timespan inventory has timespan that satisfies `timespan_inequality`::

            >>> timespan_1 = timetools.expr_to_timespan((2, 8))
            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.has_timespan_that_satisfies_inequality(timespan_inequality)
            True

        Otherwise false::

            >>> timespan_1 = timetools.expr_to_timespan((10, 20))
            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.has_timespan_that_satisfies_inequality(timespan_inequality)
            False

        Return boolean.
        '''
        return bool(self.get_timespans_that_satisfy_inequality(timespan_inequality))

    def keep_material_that_intersects_timespan(self, keep_timespan):
        from experimental import timetools
        for timespan_1 in self[:]:
            if timetools.timespan_2_contains_timespan_1_improperly(timespan_1, keep_timespan):
                pass
            elif not timetools.timespan_2_intersects_timespan_1(timespan_1, keep_timespan):
                self.remove(timespan_1)
            elif timetools.timespan_2_delays_timespan_1(timespan_1, keep_timespan):
                timespan_1.trim_to_stop_offset(keep_timespan.stop_offset)
            elif timetools.timespan_2_curtails_timespan_1(timespan_1, keep_timespan):
                timespan_1.trim_to_start_offset(keep_timespan.start_offset)
            elif timetools.timespan_2_trisects_timespan_1(timespan_1, keep_timespan):
                timespan_1.trim_to_start_offset(keep_timespan.start_offset)
                timespan_1.trim_to_stop_offset(keep_timespan.stop_offset)
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
            self[-1].trim_to_stop_offset(stop_offset)

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
                    #left_timespan, right_timespan = timespan.fracture(elements_to_move)
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

    def translate_timespans(self, addendum):
        '''Translate every timespan in inventory by `addendum`.
        
        Operate in place and return none.
        '''
        for timespan in self:
            timespan._start_offset = durationtools.Offset(timespan.start_offset + addendum)
            timespan._stop_offset = durationtools.Offset(timespan.stop_offset + addendum)

    def trim_to_start_offset(self, start_offset):
        '''Operate in place and return none.
        '''
        start_offset = durationtools.Offset(start_offset)
        assert self.start_offset <= start_offset
        delete_timespan = durationtools.TimespanConstant(self.start_offset, start_offset)
        self.delete_material_that_intersects_timespan(delete_timespan)

    def trim_to_stop_offset(self, stop_offset):
        '''Operate in place and return none.
        '''
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset <= self.stop_offset
        delete_timespan = durationtools.TimespanConstant(stop_offset, self.stop_offset)
        self.delete_material_that_intersects_timespan(delete_timespan)
