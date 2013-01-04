import copy
import math
from abjad.tools import durationtools
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class TimespanInventory(ObjectInventory):
    r'''Timespan inventory.

    Example 1::

        >>> timespan_inventory_1 = timespantools.TimespanInventory()
        >>> timespan_inventory_1.append(timespantools.Timespan(0, 3))
        >>> timespan_inventory_1.append(timespantools.Timespan(3, 6))
        >>> timespan_inventory_1.append(timespantools.Timespan(6, 10))

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

        >>> timespan_inventory_2 = timespantools.TimespanInventory()
        >>> timespan_inventory_2.append(timespantools.Timespan(0, 10))
        >>> timespan_inventory_2.append(timespantools.Timespan(3, 6))
        >>> timespan_inventory_2.append(timespantools.Timespan(15, 20))

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

    Example 3::

        >>> timespan_inventory_3 = timespantools.TimespanInventory()

    ::

        >>> z(timespan_inventory_3)
        timespantools.TimespanInventory([])

    Operations on timespan inventories currently work in place.
    
    This will change such that operations will emity a newly constructed timespan inventory.
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
        '''True when all elements in inventory are time-contiguous::

            >>> timespan_inventory_1.all_are_contiguous
            True

        False when elements in inventory are not time-contiguous::

            >>> timespan_inventory_2.all_are_contiguous
            False

        True when inventory is empty::

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
        '''True when all timespans in inventory are well-formed::

            >>> timespan_inventory_1.all_are_well_formed
            True

        ::
        
            >>> timespan_inventory_2.all_are_well_formed
            True

        Also true when inventory is empty::

            >>> timespan_inventory_3.all_are_well_formed
            True

        Otherwise false.

        Return boolean.
        '''
        return all([timespan.is_well_formed for timespan in self])

    @property
    def axis(self):
        '''Arithmetic mean of inventory start- and stop-offsets.

            >>> timespan_inventory_1.axis
            Offset(5, 1)

        ::

            >>> timespan_inventory_2.axis
            Offset(10, 1)

        None when inventory is empty::

            >>> timespan_inventory_3.axis is None
            True

        Return offset or none.
        '''
        if self:
            return (self.start_offset + self.stop_offset) / 2

    @property
    def duration(self):
        '''Time from inventory start offset to inventory stop offset::

            >>> timespan_inventory_1.duration
            Duration(10, 1)

        ::

            >>> timespan_inventory_2.duration
            Duration(20, 1)

        Zero when inventory is empty::

            >>> timespan_inventory_3.duration
            Duration(0, 1)

        Return duration.
        '''
        if self.stop_offset is not None and self.start_offset is not None:
            return self.stop_offset - self.start_offset
        else:
            return durationtools.Duration(0)

    @property
    def start_offset(self):
        '''Earliest start offset of any timespan in inventory::

            >>> timespan_inventory_1.start_offset
            Offset(0, 1)

        ::

            >>> timespan_inventory_2.start_offset
            Offset(0, 1)

        None when inventory is empty::

            >>> timespan_inventory_3.start_offset is None
            True
            
        Return offset or none.
        '''
        if self:
            return min([timespan.start_offset for timespan in self])

    @property
    def stop_offset(self):
        '''Latest stop offset of any timespan in inventory::

            >>> timespan_inventory_1.stop_offset
            Offset(10, 1)

        ::

            >>> timespan_inventory_2.stop_offset
            Offset(20, 1)
            
        None when inventory is empty::

            >>> timespan_inventory_3.stop_offset is None
            True

        Return offset or none.
        '''
        if self:
            return max([timespan.stop_offset for timespan in self])

    ### PUBLIC METHODS ###

    # TODO: do not operate in place; emit new inventory instead.
    def crop(self, start_offset=None, stop_offset=None):
        '''Operate in place.

        .. note:: add example.

        Return none.
        '''
        if start_offset is not None:
            raise NotImplementedError
        stop_offset = durationtools.Offset(stop_offset)
        inventory_stop_offset = self.stop_offset
        if stop_offset < inventory_stop_offset:
            self._set_stop_offset(stop_offset)
        elif inventory_stop_offset < stop_offset:
            self.repeat_to_stop_offset(stop_offset)

    # TODO: do not operate in place; emit new inventory instead.
    def delete_material_that_intersects_timespan(self, timespan_2):
        '''Operate in place and return none.

        .. note:: add example.

        Return none.
        '''
        for timespan_1 in self[:]:
            if timespan_2.curtails_expr(timespan_1):
                timespan_1.set_offsets(stop_offset=timespan_2.start_offset)
            elif timespan_2.delays_expr(timespan_1):
                timespan_1.set_offsets(start_offset=timespan_2.stop_offset)
            elif timespan_2.contains_expr_improperly(timespan_1):
                self.remove(timespan_1)

    # TODO: do not operate in place; emit new inventory instead.
    def fuse(self):
        '''Fuse timespans if all are contiguous.

            >>> example_inventory = timespantools.TimespanInventory()

        ::

            >>> example_inventory.append(timespantools.Timespan(0, 3))
            >>> example_inventory.append(timespantools.Timespan(3, 6))
            >>> example_inventory.append(timespantools.Timespan(6, 10))

        ::

            >>> example_inventory.fuse()

        ::

            >>> z(example_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        Operate in-place and return none.

        Raise exception on noncontiguous timespans.
        '''
        assert self.all_are_contiguous, repr(self)
        if len(self) == 0:
            return
        result = self[0]
        for timespan in self[1:]:
            result = result.fuse(timespan)
        self[:] = [result]

    def get_timespan_that_satisfies_time_relation(self, time_relation):
        r'''Get timespan that satisifies `time_relation`::

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
        r'''Get timespans that satisfy `time_relation`::

            >>> timespan_1 = timespantools.Timespan(2, 8)
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespans = timespan_inventory_1.get_timespans_that_satisfy_time_relation(time_relation)

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

            >>> timespan_1 = timespantools.Timespan(2, 8)
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory_1.has_timespan_that_satisfies_time_relation(time_relation)
            True

        Otherwise false::

            >>> timespan_1 = timespantools.Timespan(10, 20)
            >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory_1.has_timespan_that_satisfies_time_relation(time_relation)
            False

        Return boolean.
        '''
        return bool(self.get_timespans_that_satisfy_time_relation(time_relation))

    # TODO: do not operate in place; emit new inventory instead.
    def keep_material_that_intersects_timespan(self, keep_timespan):
        '''Operate in place.

        .. note:: add example.

        Return none.
        '''
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

    # TODO: remove from TimespanInventory? Implement on spectools class that inherits from TimespanInventory?
    # TODO: do not operate in place; emit new inventory instead.
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

    # TODO: move timespan.reverse() call to spectools TimespanInventory subclass
    # TODO: do not operate in place; emit new inventory instead.
    def reverse(self):
        '''Flip timespans about time axis.

        Also reverse timespans' contents.

        .. note:: add example.

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

    # TODO: remove and implement on TimespanInventory subclass in spectools instead?
    # TODO: do not operate in place; emit new inventory instead.
    def rotate(self, rotation):
        '''Rotate *elements* of timespans.

        .. note:: add example.
        
        Operation only makes sense if timespans are contiguous.

        Operate in place and return none.
        '''
        assert isinstance(rotation, int)
        assert self.all_are_contiguous
        elements_to_move = rotation % self.duration
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

    def scale(self, multiplier):
        '''Scale timespan durations by `multiplier`, keeping their start offsets constant:

            >>> example_inventory = timespantools.TimespanInventory()

        ::

            >>> example_inventory.append(timespantools.Timespan(5, 15))
            >>> example_inventory.append(timespantools.Timespan(10, 20))
            >>> example_inventory.append(timespantools.Timespan(25, 30))

        ::

            >>> example_inventory.scale(2)

        ::

            >>> z(example_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Duration(25, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Duration(30, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(25, 1),
                    stop_offset=durationtools.Duration(35, 1)
                    )
                ])

        Operate in place and return none.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        assert 0 < multiplier
        for timespan in self:
            timespan._stop_offset = (timespan.duration * multiplier) + timespan._start_offset

    def stretch(self, multiplier):
        '''Stretch timespans by `multiplier`, keeping the earliest start offset constant:

        ::

            >>> example_inventory = timespantools.TimespanInventory()

        ::

            >>> example_inventory.append(timespantools.Timespan(5, 15))
            >>> example_inventory.append(timespantools.Timespan(10, 20))
            >>> example_inventory.append(timespantools.Timespan(25, 30))

        ::

            >>> example_inventory.stretch(2)

        ::

            >>> z(example_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(25, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(15, 1),
                    stop_offset=durationtools.Offset(35, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(45, 1),
                    stop_offset=durationtools.Offset(55, 1)
                    )
                ])

        Operate in place and return none.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        assert 0 < multiplier
        if not len(self):
            return
        inventory_start_offset = self.start_offset
        for timespan in self:
            start_offset, duration = timespan.start_offset, timespan.duration
            timespan._start_offset = durationtools.Offset(
                ((start_offset - inventory_start_offset) * multiplier) + inventory_start_offset)
            timespan._stop_offset = durationtools.Offset(
                (duration * multiplier) + timespan._start_offset)

    # TODO: do not operate in place; emit new inventory instead.
    def translate_offsets(self, start_offset_translation=None, stop_offset_translation=None):
        '''Translate every timespan in inventory by `start_offset_translation`
        and `stop_offset_translation`.

        .. note:: add example.
        
        Operate in place and return none.
        '''
        for timespan in self:
            if start_offset_translation is not None:
                timespan._start_offset = durationtools.Offset(timespan.start_offset + start_offset_translation)
            if stop_offset_translation is not None:
                timespan._stop_offset = durationtools.Offset(timespan.stop_offset + stop_offset_translation)
