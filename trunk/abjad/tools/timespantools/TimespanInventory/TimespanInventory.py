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

    def delete_material_that_intersects_timespan(self, timespan_2):
        '''Operate in place and return timespan inventory.

        .. note:: function does not yet work on (pure) TimespanInventory objects.
                  function works on only TimespanInventory subclasses.

        Return none.
        '''
        for timespan in self[:]:
            if timespan_2.curtails_timespan(timespan):
                timespan.set_offsets(stop_offset=timespan_2.start_offset)
            elif timespan_2.delays_timespan(timespan):
                timespan.set_offsets(start_offset=timespan_2.stop_offset)
            elif timespan_2.contains_timespan_improperly(timespan):
                self.remove(timespan)

    def compute_logical_and(self):
        '''Compute logical AND of timespans.

        Operate in place and return timespan inventory.
        '''
    def fuse(self):
        '''Compute logical OR of timespans in inventory:

        ::

            >>> z(timespan_inventory_1.fuse())
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        ::

            >>> z(timespan_inventory_2.fuse())
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(15, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                ])

        ::

            >>> z(timespan_inventory_3.fuse())
            timespantools.TimespanInventory([])

        Emity newly constructed timespan inventory.
        '''
        new_timespans = []
        if self:
            new_timespans.append(copy.deepcopy(self[0]))
            for timespan in self[1:]:
                if new_timespans[-1].can_fuse(timespan):
                    new_timespan = new_timespans[-1].fuse(timespan)
                    new_timespans[-1] = new_timespan
                else:
                    new_timespans.append(copy.deepcopy(timespan))
        return type(self)(new_timespans)

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

        Example 1. Translate timespan by offset ``50``::.

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

    def trim_to_timespan(self, timespan):
        '''Keep material that intersects `timespan`:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10)])

        ::  

            >>> timespan = timespantools.Timespan(2, 7)
            >>> result = timespan_inventory.trim_to_timespan(timespan)

        ::

            >>> z(timespan_inventory)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(2, 1),
                    stop_offset=durationtools.Offset(3, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(3, 1),
                    stop_offset=durationtools.Offset(6, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(6, 1),
                    stop_offset=durationtools.Offset(7, 1)
                    )
                ])

        Operate in place and return none.
        '''
        timespans = []
        for current_timespan in self:
            if timespan.contains_timespan_improperly(current_timespan):
                pass
            elif not timespan.intersects_timespan(current_timespan):
                continue
            elif timespan.delays_timespan(current_timespan):
                current_timespan = current_timespan.set_offsets(stop_offset=timespan.stop_offset)
            elif timespan.curtails_timespan(current_timespan):
                current_timespan = current_timespan.set_offsets(start_offset=timespan.start_offset)
            elif timespan.trisects_timespan(current_timespan):
                current_timespan = current_timespan.set_offsets(*timespan.offsets)
            else:
                raise ValueError(current_timespan)
            assert current_timespan is not None
            timespans.append(current_timespan)
        self[:] = timespans
        return self
