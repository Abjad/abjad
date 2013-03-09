import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from abjad.tools.mathtools.BoundedObject import BoundedObject


class Timespan(BoundedObject):
    r'''Closed-open interval.

    Examples:

    ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 12)
            >>> timespan_3 = timespantools.Timespan(-2, 2)
            >>> timespan_4 = timespantools.Timespan(10, 20)

    Timespans are immutable and treated as value objects.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_start_offset', '_stop_offset',
        )

    ### INITIALIZER ###

    def __init__(self, start_offset=NegativeInfinity, stop_offset=Infinity):
        BoundedObject.__init__(self)
        start_offset = self._initialize_offset(start_offset)
        stop_offset = self._initialize_offset(stop_offset)
        assert start_offset is not None
        assert stop_offset is not None
        assert start_offset <= stop_offset, repr((start_offset, stop_offset))
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### SPECIAL METHODS ###

    def __and__(self, expr):
        '''Logical AND of two timespans:

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 12)
            >>> timespan_3 = timespantools.Timespan(-2, 2)
            >>> timespan_4 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1 & timespan_2
            TimespanInventory([Timespan(start_offset=Offset(5, 1), stop_offset=Offset(10, 1))])

        ::

            >>> timespan_1 & timespan_3
            TimespanInventory([Timespan(start_offset=Offset(0, 1), stop_offset=Offset(2, 1))])

        ::

            >>> timespan_1 & timespan_4
            TimespanInventory([])

        ::

            >>> timespan_2 & timespan_3
            TimespanInventory([])

        ::

            >>> timespan_2 & timespan_4
            TimespanInventory([Timespan(start_offset=Offset(10, 1), stop_offset=Offset(12, 1))])

        ::

            >>> timespan_3 & timespan_4
            TimespanInventory([])

        Return timespan inventory.
        '''
        from abjad.tools import timespantools
        expr = self._get_timespan(expr)
        if not self.intersects_timespan(expr):
            return timespantools.TimespanInventory()
        new_start_offset = max(self.start_offset, expr.start_offset)
        new_stop_offset = min(self.stop_offset, expr.stop_offset)
        timespan = type(self)(new_start_offset, new_stop_offset)
        return timespantools.TimespanInventory([timespan])

    def __eq__(self, timespan):
        '''True when `timespan` is a timespan with equal offsets::

            >>> timespantools.Timespan(1, 3) == timespantools.Timespan(1, 3)
            True

        Otherwise false::

            >>> timespantools.Timespan(1, 3) == timespantools.Timespan(2, 3)
            False

        Return boolean.
        '''
        if isinstance(timespan, type(self)):
            return self.offsets == timespan.offsets
        return False

    def __ge__(self, expr):
        '''True when `expr` start offset is greater or equal to timespan start offset:

        ::

            >>> timespan_2 >= timespan_3
            True

        Otherwise false:

        ::

            >>> timespan_1 >= timespan_2
            False

        Return boolean.
        '''
        assert hasattr(expr, 'start_offset'), repr(expr)
        if hasattr(expr, 'stop_offset'):
            if self.start_offset >= expr.start_offset:
                return True
            elif self.start_offset == expr.start_offset and \
                self.stop_offset >= expr.stop_offset:
                return True
            return False
        return self.start_offset >= expr.start_offset

    def __gt__(self, expr):
        '''True when `expr` start offset is greater than timespan start offset:

        ::

            >>> timespan_2 > timespan_3
            True

        Otherwise false:

        ::

            >>> timespan_1 > timespan_2
            False

        Return boolean.
        '''
        assert hasattr(expr, 'start_offset'), repr(expr)
        if hasattr(expr, 'stop_offset'):
            if self.start_offset > expr.start_offset:
                return True
            elif self.start_offset == expr.start_offset and \
                self.stop_offset > expr.stop_offset:
                return True
            return False
        return self.start_offset > expr.start_offset

    def __le__(self, expr):
        '''True when `expr` start offset is less than or equal to timespan start offset:

        ::

            >>> timespan_2 <= timespan_3
            False

        Otherwise false:

        ::

            >>> timespan_1 <= timespan_2
            True

        Return boolean.
        '''
        assert hasattr(expr, 'start_offset'), repr(expr)
        if hasattr(expr, 'stop_offset'):
            if self.start_offset <= expr.start_offset:
                return True
            elif self.start_offset == expr.start_offset and \
                self.stop_offset <= expr.stop_offset:
                return True
            return False
        return self.start_offset <= expr.start_offset

    def __len__(self):
        '''Defined equal to ``1`` for all timespans:

        ::

            >>> len(timespan_1)
            1

        Return positive integer.
        '''
        return 1

    def __lt__(self, expr):
        '''True when `expr` start offset is less than timespan start offset:

        ::

            >>> timespan_1 < timespan_2
            True

        Otherwise false:

        ::

            >>> timespan_2 < timespan_3
            False

        Return boolean.
        '''
        assert hasattr(expr, 'start_offset'), repr(expr)
        if hasattr(expr, 'stop_offset'):
            if self.start_offset < expr.start_offset:
                return True
            elif self.start_offset == expr.start_offset and \
                self.stop_offset < expr.stop_offset:
                return True
            return False
        return self.start_offset < expr.start_offset

    def __ne__(self, timespan):
        '''True when `timespan` is not a timespan with equivalent offsets::

            >>> timespantools.Timespan(1, 3) != timespantools.Timespan(2, 3)
            True

        Otherwise false::

            >>> timespantools.Timespan(1, 3) != timespantools.Timespan(2/2, (3, 1))
            False

        Return boolean.
        '''
        return not self == timespan

    def __or__(self, expr):
        '''Logical OR of two timespans:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 12)
            >>> timespan_3 = timespantools.Timespan(-2, 2)
            >>> timespan_4 = timespantools.Timespan(10, 20)

        ::

            >>> z(timespan_1 | timespan_2)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    )
                ])

        ::

            >>> z(timespan_1 | timespan_3)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        ::


            >>> z(timespan_1 | timespan_4)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                ])

        ::

            >>> z(timespan_2 | timespan_3)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    )
                ])

        ::

            >>> z(timespan_2 | timespan_4)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                ])

        ::

            >>> z(timespan_3 | timespan_4)
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

        Return timespan inventory.
        '''
        from abjad.tools import timespantools
        expr = self._get_timespan(expr)
        if not self.intersects_timespan(expr) and \
            not self.is_tangent_to_timespan(expr):
            result = timespantools.TimespanInventory([self, expr])
            result.sort()
            return result
        new_start_offset = min(self.start_offset, expr.start_offset)
        new_stop_offset = max(self.stop_offset, expr.stop_offset)
        timespan = type(self)(new_start_offset, new_stop_offset)
        return timespantools.TimespanInventory([timespan])

    def __repr__(self):
        '''Interpreter representation of timespan:

        ::

            >>> timespan_1
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        Return string.
        '''
        return BoundedObject.__repr__(self)

    def __sub__(self, expr):
        '''Subtract `expr` from timespan:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 12)
            >>> timespan_3 = timespantools.Timespan(-2, 2)
            >>> timespan_4 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1 - timespan_1
            TimespanInventory([])

        ::

            >>> timespan_1 - timespan_2
            TimespanInventory([Timespan(start_offset=Offset(0, 1), stop_offset=Offset(5, 1))])

        ::

            >>> timespan_1 - timespan_3
            TimespanInventory([Timespan(start_offset=Offset(2, 1), stop_offset=Offset(10, 1))])

        ::

            >>> timespan_1 - timespan_4
            TimespanInventory([Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))])

        ::

            >>> timespan_2 - timespan_1
            TimespanInventory([Timespan(start_offset=Offset(10, 1), stop_offset=Offset(12, 1))])

        ::

            >>> timespan_2 - timespan_2
            TimespanInventory([])

        ::

            >>> timespan_2 - timespan_3
            TimespanInventory([Timespan(start_offset=Offset(5, 1), stop_offset=Offset(12, 1))])

        ::

            >>> timespan_2 - timespan_4
            TimespanInventory([Timespan(start_offset=Offset(5, 1), stop_offset=Offset(10, 1))])

        ::

            >>> timespan_3 - timespan_3
            TimespanInventory([])

        ::

            >>> timespan_3 - timespan_1
            TimespanInventory([Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(0, 1))])

        ::

            >>> timespan_3 - timespan_2
            TimespanInventory([Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(2, 1))])

        ::

            >>> timespan_3 - timespan_4
            TimespanInventory([Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(2, 1))])

        ::

            >>> timespan_4 - timespan_4
            TimespanInventory([])

        ::

            >>> timespan_4 - timespan_1
            TimespanInventory([Timespan(start_offset=Offset(10, 1), stop_offset=Offset(20, 1))])

        ::

            >>> timespan_4 - timespan_2
            TimespanInventory([Timespan(start_offset=Offset(12, 1), stop_offset=Offset(20, 1))])

        ::

            >>> timespan_4 - timespan_3
            TimespanInventory([Timespan(start_offset=Offset(10, 1), stop_offset=Offset(20, 1))])

        Return timespan inventory.
        '''
        from abjad.tools import timespantools
        expr = self._get_timespan(expr)
        inventory = timespantools.TimespanInventory()
        if not self.intersects_timespan(expr):
            inventory.append(copy.deepcopy(self))
        elif expr.trisects_timespan(self):
            new_start_offset = self.start_offset
            new_stop_offset = expr.start_offset
            timespan = type(self)(new_start_offset, new_stop_offset)
            inventory.append(timespan)
            new_start_offset = expr.stop_offset
            new_stop_offset = self.stop_offset
            timespan = type(self)(new_start_offset, new_stop_offset)
            inventory.append(timespan)
        elif expr.contains_timespan_improperly(self):
            pass
        elif expr.overlaps_only_start_of_timespan(self):
            new_start_offset = expr.stop_offset
            new_stop_offset = self.stop_offset
            timespan = type(self)(new_start_offset, new_stop_offset)
            inventory.append(timespan)
        elif expr.overlaps_only_stop_of_timespan(self):
            new_start_offset = self.start_offset
            new_stop_offset = expr.start_offset
            timespan = type(self)(new_start_offset, new_stop_offset)
            inventory.append(timespan)
        elif expr.starts_when_timespan_starts(self) and \
            expr.stops_before_timespan_stops(self):
            new_start_offset = expr.stop_offset
            new_stop_offset = self.stop_offset
            timespan = type(self)(new_start_offset, new_stop_offset)
            inventory.append(timespan)
        elif expr.stops_when_timespan_stops(self) and \
            expr.starts_after_timespan_starts(self):
            new_start_offset = self.start_offset
            new_stop_offset = expr.start_offset
            timespan = type(self)(new_start_offset, new_stop_offset)
            inventory.append(timespan)
        else:
            raise ValueError(self, expr)
        return inventory

    def __xor__(self, expr):
        '''Logical AND of two timespans:

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 12)
            >>> timespan_3 = timespantools.Timespan(-2, 2)
            >>> timespan_4 = timespantools.Timespan(10, 20)

        ::

            >>> z(timespan_1 ^ timespan_2)
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

        ::

            >>> z(timespan_1 ^ timespan_3)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(0, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(2, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    )
                ])

        ::

            >>> z(timespan_1 ^ timespan_4)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                ])

        ::

            >>> z(timespan_2 ^ timespan_3)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    )
                ])

        ::

            >>> z(timespan_2 ^ timespan_4)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(12, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    )
                ])

        ::

            >>> z(timespan_3 ^ timespan_4)
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

        Return timespan inventory.
        '''
        from abjad.tools import timespantools
        expr = self._get_timespan(expr)
        if not self.intersects_timespan(expr) or \
            self.is_tangent_to_timespan(expr):
            result = timespantools.TimespanInventory()
            result.append(copy.deepcopy(self))
            result.append(copy.deepcopy(expr))
            result.sort()
            return result
        result = timespantools.TimespanInventory()
        start_offsets = [self.start_offset, expr.start_offset]
        stop_offsets = [self.stop_offset, expr.stop_offset]
        start_offsets.sort()
        stop_offsets.sort()
        timespan_1 = type(self)(*start_offsets)
        timespan_2 = type(self)(*stop_offsets)
        if timespan_1.is_well_formed:
            result.append(timespan_1)
        if timespan_2.is_well_formed:
            result.append(timespan_2)
        result.sort()
        return result

    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        if isinstance(expr, type(self)):
            return self.intersects_timespan(expr) or self.stops_when_timespan_starts(expr)
        return False

    def _get_offsets(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return expr.start_offset, expr.stop_offset
        elif hasattr(expr, 'timespan'):
            return expr.timespan.offsets
        else:
            raise TypeError(expr)

    def _get_timespan(self, expr):
        start_offset, stop_offset = self._get_offsets(expr)
        return type(self)(start_offset, stop_offset)

    def _implements_timespan_interface(self, timespan):
        if hasattr(timespan, 'start_offset') and hasattr(timespan, 'stop_offset'):
            return True
        if hasattr(timespan, 'timespan'):
            return True
        return False

    def _initialize_offset(self, offset):
        if offset in (NegativeInfinity, Infinity):
            return offset
        else:
            return durationtools.Offset(offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def axis(self):
        '''Arithmetic mean of timespan start- and stop-offsets::

            >>> timespan_1.axis
            Offset(5, 1)

        Return offset.
        '''
        return (self.start_offset + self.stop_offset) / 2

    @property
    def duration(self):
        '''Get timespan duration::

            >>> timespan_1.duration
            Duration(10, 1)

        Return duration.
        '''
        return self.stop_offset - self.start_offset

    @property
    def is_closed(self):
        '''False for all timespans:

        ::

            >>> timespan_1.is_closed
            False

        Return boolean.
        '''
        return BoundedObject.is_closed.fget(self)

    @property
    def is_half_closed(self):
        '''True for all timespans:

        ::

            >>> timespan_1.is_half_closed
            True

        Return boolean.
        '''
        return BoundedObject.is_half_closed.fget(self)

    @property
    def is_half_open(self):
        '''True for all timespans:

        ::

            >>> timespan_1.is_half_open
            True

        Return boolean.
        '''
        return BoundedObject.is_half_open.fget(self)

    @property
    def is_left_closed(self):
        '''True for all timespans.

            >>> timespan_1.is_left_closed
            True

        Return boolean.
        '''
        return True


    @property
    def is_left_open(self):
        '''False for all timespans.

            >>> timespan_1.is_left_open
            False

        Return boolean.
        '''
        return False

    @property
    def is_open(self):
        '''False for all timespans:

        ::

            >>> timespan_1.is_open
            False

        Return boolean.
        '''
        return BoundedObject.is_open.fget(self)

    @property
    def is_right_closed(self):
        '''False for all timespans.

            >>> timespan_1.is_right_closed
            False

        Return boolean.
        '''
        return False


    @property
    def is_right_open(self):
        '''True for all timespans.

            >>> timespan_1.is_right_open
            True

        Return boolean.
        '''
        return True

    @property
    def is_well_formed(self):
        '''True when timespan start offset preceeds timespan stop offset.
        Otherwise false::

            >>> timespan_1.is_well_formed
            True

        Return boolean.
        '''
        return self.start_offset < self.stop_offset

    @property
    def offsets(self):
        '''Timespan offsets::

            >>> timespan_1.offsets
            (Offset(0, 1), Offset(10, 1))

        Return offset pair.
        '''
        return self.start_offset, self.stop_offset

    @property
    def start_offset(self):
        '''Timespan start offset::

            >>> timespan_1.start_offset
            Offset(0, 1)

        Return offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Timespan stop offset::

            >>> timespan_1.stop_offset
            Offset(10, 1)

        Return offset.
        '''
        return self._stop_offset

    @property
    def storage_format(self):
        '''Timespan storage format:

        ::

            >>> z(timespan_1)
            timespantools.Timespan(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(10, 1)
                )

        Return string.
        '''

    ### PUBLIC METHODS ###

    def contains_timespan_improperly(self, timespan):
        '''True when timespan contains `timespan` improperly. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 10)

        ::

            >>> timespan_1.contains_timespan_improperly(timespan_1)
            True
            >>> timespan_1.contains_timespan_improperly(timespan_2)
            True
            >>> timespan_2.contains_timespan_improperly(timespan_1)
            False
            >>> timespan_2.contains_timespan_improperly(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_contains_timespan_1_improperly(timespan, self)

    def curtails_timespan(self, timespan):
        '''True when timespan curtails `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 10)

        ::

            >>> timespan_1.curtails_timespan(timespan_1)
            False
            >>> timespan_1.curtails_timespan(timespan_2)
            False
            >>> timespan_2.curtails_timespan(timespan_1)
            True
            >>> timespan_2.curtails_timespan(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_curtails_timespan_1(timespan, self)

    def delays_timespan(self, timespan):
        '''True when timespan delays `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)
            >>> timespan_3 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.delays_timespan(timespan_2)
            True
            >>> timespan_2.delays_timespan(timespan_3)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_delays_timespan_1(timespan, self)

    def divide_by_ratio(self, ratio):
        '''Divide timespan by `ratio`::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2))

        ::

            >>> for x in timespan.divide_by_ratio((1, 2, 1)):
            ...     x
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(3, 4))
            Timespan(start_offset=Offset(3, 4), stop_offset=Offset(5, 4))
            Timespan(start_offset=Offset(5, 4), stop_offset=Offset(3, 2))

        Return tuple of newly constructed timespans.
        '''
        if isinstance(ratio, int):
            ratio = ratio * (1, )
        ratio = mathtools.Ratio(ratio)
        unit_duration = self.duration / sum(ratio)
        part_durations = [numerator * unit_duration for numerator in ratio]
        start_offsets = mathtools.cumulative_sums([self.start_offset] + part_durations)
        offset_pairs = sequencetools.iterate_sequence_pairwise_strict(start_offsets)
        result = [type(self)(*offset_pair) for offset_pair in offset_pairs]
        return tuple(result)

    def happens_during_timespan(self, timespan):
        '''True when timespan happens during `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 10)

        ::

            >>> timespan_1.happens_during_timespan(timespan_1)
            True
            >>> timespan_1.happens_during_timespan(timespan_2)
            False
            >>> timespan_2.happens_during_timespan(timespan_1)
            True
            >>> timespan_2.happens_during_timespan(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_happens_during_timespan_1(timespan, self)

    def intersects_timespan(self, timespan):
        '''True when timespan intersects `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)
            >>> timespan_3 = timespantools.Timespan(10, 15)

        ::

            >>> timespan_1.intersects_timespan(timespan_1)
            True
            >>> timespan_1.intersects_timespan(timespan_2)
            True
            >>> timespan_1.intersects_timespan(timespan_3)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_intersects_timespan_1(timespan, self)

    def is_congruent_to_timespan(self, timespan):
        '''True when timespan is congruent to `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.is_congruent_to_timespan(timespan_1)
            True
            >>> timespan_1.is_congruent_to_timespan(timespan_2)
            False
            >>> timespan_2.is_congruent_to_timespan(timespan_1)
            False
            >>> timespan_2.is_congruent_to_timespan(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_is_congruent_to_timespan_1(timespan, self)

    def is_tangent_to_timespan(self, timespan):
        '''True when timespan is tangent to `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.is_tangent_to_timespan(timespan_1)
            False
            >>> timespan_1.is_tangent_to_timespan(timespan_2)
            True
            >>> timespan_2.is_tangent_to_timespan(timespan_1)
            True
            >>> timespan_2.is_tangent_to_timespan(timespan_2)
            False

        Return boolean.
        '''
        if hasattr(timespan, 'start_offset'):
            if self.stop_offset == timespan.start_offset:
                return True
        if hasattr(timespan, 'stop_offset'):
            if timespan.stop_offset == self.start_offset:
                return True
        return False

    def new(self, **kwargs):
        '''Create new timespan with `kwargs`:

        ::

            >>> timespan_1.new(stop_offset=Offset(9))
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 1))

        Return new timespan.
        '''
        positional_argument_dictionary = self._positional_argument_dictionary
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        for positional_argument_name in self._positional_argument_names:
            positional_argument_value = positional_argument_dictionary[positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(self)(*positional_argument_values, **keyword_argument_dictionary)
        return result

    def overlaps_all_of_timespan(self, timespan):
        '''True when timespan overlaps all of `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 6)
            >>> timespan_3 = timespantools.Timespan(5, 10)

        ::

            >>> timespan_1.overlaps_all_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_all_of_timespan(timespan_2)
            True
            >>> timespan_1.overlaps_all_of_timespan(timespan_3)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_all_of_timespan_1(timespan, self)

    def overlaps_only_start_of_timespan(self, timespan):
        '''True when timespan overlaps only start of `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(-5, 5)
            >>> timespan_3 = timespantools.Timespan(4, 6)
            >>> timespan_4 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.overlaps_only_start_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_only_start_of_timespan(timespan_2)
            False
            >>> timespan_1.overlaps_only_start_of_timespan(timespan_3)
            False
            >>> timespan_1.overlaps_only_start_of_timespan(timespan_4)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_only_start_of_timespan_1(timespan, self)

    def overlaps_only_stop_of_timespan(self, timespan):
        '''True when timespan overlaps only stop of `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(-5, 5)
            >>> timespan_3 = timespantools.Timespan(4, 6)
            >>> timespan_4 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.overlaps_only_stop_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_only_stop_of_timespan(timespan_2)
            True
            >>> timespan_1.overlaps_only_stop_of_timespan(timespan_3)
            False
            >>> timespan_1.overlaps_only_stop_of_timespan(timespan_4)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_only_stop_of_timespan_1(timespan, self)

    def overlaps_start_of_timespan(self, timespan):
        '''True when timespan overlaps start of `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(-5, 5)
            >>> timespan_3 = timespantools.Timespan(4, 6)
            >>> timespan_4 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.overlaps_start_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_start_of_timespan(timespan_2)
            False
            >>> timespan_1.overlaps_start_of_timespan(timespan_3)
            True
            >>> timespan_1.overlaps_start_of_timespan(timespan_4)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_start_of_timespan_1(timespan, self)

    def overlaps_stop_of_timespan(self, timespan):
        '''True when timespan overlaps start of `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(-5, 5)
            >>> timespan_3 = timespantools.Timespan(4, 6)
            >>> timespan_4 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.overlaps_stop_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_stop_of_timespan(timespan_2)
            True
            >>> timespan_1.overlaps_stop_of_timespan(timespan_3)
            True
            >>> timespan_1.overlaps_stop_of_timespan(timespan_4)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_stop_of_timespan_1(timespan, self)

    def reflect(self, axis=None):
        '''Reverse timespan about `axis`.

        Example 1. Reverse timespan about timespan axis:

        ::

            >>> timespantools.Timespan(3, 6).reflect()
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        Example 2. Reverse timespan about arbitrary axis:

        ::

            >>> timespantools.Timespan(3, 6).reflect(axis=Offset(10))
            Timespan(start_offset=Offset(14, 1), stop_offset=Offset(17, 1))

        Emit newly constructed timespan.
        '''
        if axis is None:
            axis = self.axis
        start_distance = self.start_offset - axis
        stop_distance = self.stop_offset - axis
        new_start_offset = axis - stop_distance
        new_stop_offset = axis - start_distance
        return self.set_offsets(new_start_offset, new_stop_offset)

    def scale(self, multiplier, anchor=Left):
        '''Scale timespan by `multiplier`.

            >>> timespan = timespantools.Timespan(3, 6)

        Example 1. Scale timespan relative to timespan start offset:

        ::

            >>> timespan.scale(Multiplier(2))
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(9, 1))

        Example 2. Scale timespan relative to timespan stop offset:

        ::

            >>> timespan.scale(Multiplier(2), anchor=Right)
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(6, 1))


        Emit newly constructed timespan.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        assert 0 < multiplier
        new_duration = multiplier * self.duration
        if anchor is Left:
            new_start_offset = self.start_offset
            new_stop_offset = self.start_offset + new_duration
        elif anchor is Right:
            new_stop_offset = self.stop_offset
            new_start_offset = self.stop_offset - new_duration
        else:
            raise ValueError
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    def set_duration(self, duration):
        '''Set timespan duration to `duration`::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2))

        ::

            >>> timespan.set_duration(Duration(3, 5))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(11, 10))

        Emit newly constructed timespan.
        '''
        duration = durationtools.Duration(duration)
        new_stop_offset = self.start_offset + duration
        result = type(self)(self.start_offset, new_stop_offset)
        return result

    def set_offsets(self, start_offset=None, stop_offset=None):
        '''Set timespan start offset to `start_offset` and
        stop offset to `stop_offset`::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2))

        ::

            >>> timespan.set_offsets(stop_offset=Offset(7, 8))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(7, 8))

        Subtract negative `start_offset` from existing stop offset::

            >>> timespan.set_offsets(start_offset=Offset(-1, 2))
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 2))

        Subtract negative `stop_offset` from existing stop offset::

            >>> timespan.set_offsets(stop_offset=Offset(-1, 2))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(1, 1))

        Emit newly constructed timespan.
        '''
        if start_offset is not None and 0 <= start_offset:
            new_start_offset = start_offset
        elif start_offset is not None and start_offset < 0:
            new_start_offset = self.stop_offset + durationtools.Offset(start_offset)
        else:
            new_start_offset = self.start_offset
        if stop_offset is not None and 0 <= stop_offset:
            new_stop_offset = stop_offset
        elif stop_offset is not None and stop_offset < 0:
            new_stop_offset = self.stop_offset + durationtools.Offset(stop_offset)
        else:
            new_stop_offset = self.stop_offset
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    # TODO: extend to self.split_at_offsets()
    def split_at_offset(self, offset):
        '''Split into two parts when `offset` happens during timespan::

            >>> timespan = timespantools.Timespan(0, 5)

        ::

            >>> left, right = timespan.split_at_offset(Offset(2))

        ::

            >>> left
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(2, 1))

        ::

            >>> right
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(5, 1))

        Otherwise return a copy of timespan::

            >>> timespan.split_at_offset(Offset(12))
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(5, 1))

        Return one or two newly constructed timespans.
        '''
        offset = durationtools.Offset(offset)
        if self.start_offset < offset < self.stop_offset:
            left = type(self)(self.start_offset, offset)
            right = type(self)(offset, self.stop_offset)
            return left, right
        else:
            return type(self)(self.start_offset, self.stop_offset)

    def starts_after_offset(self, offset):
        '''True when timespan overlaps start of `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_after_offset(Offset(-5))
            True
            >>> timespan_1.starts_after_offset(Offset(0))
            False
            >>> timespan_1.starts_after_offset(Offset(5))
            False

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return offset < self.start_offset

    def starts_after_timespan_starts(self, timespan):
        '''True when timespan starts after `timespan` starts. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.starts_after_timespan_starts(timespan_1)
            False
            >>> timespan_1.starts_after_timespan_starts(timespan_2)
            False
            >>> timespan_2.starts_after_timespan_starts(timespan_1)
            True
            >>> timespan_2.starts_after_timespan_starts(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_after_timespan_1_starts(timespan, self)

    def starts_after_timespan_stops(self, timespan):
        '''True when timespan starts after `timespan` stops. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)
            >>> timespan_3 = timespantools.Timespan(10, 20)
            >>> timespan_4 = timespantools.Timespan(15, 25)

        ::

            >>> timespan_1.starts_after_timespan_stops(timespan_1)
            False
            >>> timespan_2.starts_after_timespan_stops(timespan_1)
            False
            >>> timespan_3.starts_after_timespan_stops(timespan_1)
            True
            >>> timespan_4.starts_after_timespan_stops(timespan_1)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_after_timespan_1_stops(timespan, self)

    def starts_at_offset(self, offset):
        '''True when timespan starts at `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_at_offset(Offset(-5))
            False
            >>> timespan_1.starts_at_offset(Offset(0))
            True
            >>> timespan_1.starts_at_offset(Offset(5))
            False

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.start_offset == offset

    def starts_at_or_after_offset(self, offset):
        '''True when timespan starts at or after `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_at_or_after_offset(Offset(-5))
            True
            >>> timespan_1.starts_at_or_after_offset(Offset(0))
            True
            >>> timespan_1.starts_at_or_after_offset(Offset(5))
            False

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return offset <= self.start_offset

    def starts_before_offset(self, offset):
        '''True when timespan starts before `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_before_offset(Offset(-5))
            False
            >>> timespan_1.starts_before_offset(Offset(0))
            False
            >>> timespan_1.starts_before_offset(Offset(5))
            True

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.start_offset < offset

    def starts_before_or_at_offset(self, offset):
        '''True when timespan starts before or at `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_before_or_at_offset(Offset(-5))
            False
            >>> timespan_1.starts_before_or_at_offset(Offset(0))
            True
            >>> timespan_1.starts_before_or_at_offset(Offset(5))
            True

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.start_offset <= offset

    def starts_before_timespan_starts(self, timespan):
        '''True when timespan starts before `timespan` starts. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.starts_before_timespan_starts(timespan_1)
            False
            >>> timespan_1.starts_before_timespan_starts(timespan_2)
            True
            >>> timespan_2.starts_before_timespan_starts(timespan_1)
            False
            >>> timespan_2.starts_before_timespan_starts(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_before_timespan_1_starts(timespan, self)

    def starts_before_timespan_stops(self, timespan):
        '''True when timespan starts before `timespan` stops. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.starts_before_timespan_stops(timespan_1)
            True
            >>> timespan_1.starts_before_timespan_stops(timespan_2)
            True
            >>> timespan_2.starts_before_timespan_stops(timespan_1)
            True
            >>> timespan_2.starts_before_timespan_stops(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_before_timespan_1_stops(timespan, self)

    def starts_during_timespan(self, timespan):
        '''True when timespan starts during `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.starts_during_timespan(timespan_1)
            True
            >>> timespan_1.starts_during_timespan(timespan_2)
            False
            >>> timespan_2.starts_during_timespan(timespan_1)
            True
            >>> timespan_2.starts_during_timespan(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_during_timespan_1(timespan, self)

    def starts_when_timespan_starts(self, timespan):
        '''True when timespan starts when `timespan` starts. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)

        ::

            >>> timespan_1.starts_when_timespan_starts(timespan_1)
            True
            >>> timespan_1.starts_when_timespan_starts(timespan_2)
            False
            >>> timespan_2.starts_when_timespan_starts(timespan_1)
            False
            >>> timespan_2.starts_when_timespan_starts(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_when_timespan_1_starts(timespan, self)

    def starts_when_timespan_stops(self, timespan):
        '''True when timespan starts when `timespan` stops. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.starts_when_timespan_stops(timespan_1)
            False
            >>> timespan_1.starts_when_timespan_stops(timespan_2)
            False
            >>> timespan_2.starts_when_timespan_stops(timespan_1)
            True
            >>> timespan_2.starts_when_timespan_stops(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_when_timespan_1_stops(timespan, self)

    def stops_after_offset(self, offset):
        '''True when timespan stops after `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_after_offset(Offset(-5))
            True
            >>> timespan_1.starts_after_offset(Offset(0))
            False
            >>> timespan_1.starts_after_offset(Offset(5))
            False

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return offset < self.stop_offset

    def stops_after_timespan_starts(self, timespan):
        '''True when timespan stops when `timespan` starts. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.stops_after_timespan_starts(timespan_1)
            True
            >>> timespan_1.stops_after_timespan_starts(timespan_2)
            False
            >>> timespan_2.stops_after_timespan_starts(timespan_1)
            True
            >>> timespan_2.stops_after_timespan_starts(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_after_timespan_1_starts(timespan, self)

    def stops_after_timespan_stops(self, timespan):
        '''True when timespan stops when `timespan` stops. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.stops_after_timespan_stops(timespan_1)
            False
            >>> timespan_1.stops_after_timespan_stops(timespan_2)
            False
            >>> timespan_2.stops_after_timespan_stops(timespan_1)
            True
            >>> timespan_2.stops_after_timespan_stops(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_after_timespan_1_stops(timespan, self)

    def stops_at_offset(self, offset):
        '''True when timespan stops at `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.stops_at_offset(Offset(-5))
            False
            >>> timespan_1.stops_at_offset(Offset(0))
            False
            >>> timespan_1.stops_at_offset(Offset(5))
            False

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.stop_offset == offset

    def stops_at_or_after_offset(self, offset):
        '''True when timespan stops at or after `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.stops_at_or_after_offset(Offset(-5))
            True
            >>> timespan_1.stops_at_or_after_offset(Offset(0))
            True
            >>> timespan_1.stops_at_or_after_offset(Offset(5))
            True

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return offset <= self.stop_offset

    def stops_before_offset(self, offset):
        '''True when timespan stops before `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.stops_before_offset(Offset(-5))
            False
            >>> timespan_1.stops_before_offset(Offset(0))
            False
            >>> timespan_1.stops_before_offset(Offset(5))
            False

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.stop_offset < offset

    def stops_before_or_at_offset(self, offset):
        '''True when timespan stops before or at `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.stops_before_or_at_offset(Offset(-5))
            False
            >>> timespan_1.stops_before_or_at_offset(Offset(0))
            False
            >>> timespan_1.stops_before_or_at_offset(Offset(5))
            False

        Return boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.stop_offset <= offset

    def stops_before_timespan_starts(self, timespan):
        '''True when timespan stops before `timespan` starts. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.stops_before_timespan_starts(timespan_1)
            False
            >>> timespan_1.stops_before_timespan_starts(timespan_2)
            False
            >>> timespan_2.stops_before_timespan_starts(timespan_1)
            False
            >>> timespan_2.stops_before_timespan_starts(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_before_timespan_1_starts(timespan, self)

    def stops_before_timespan_stops(self, timespan):
        '''True when timespan stops before `timespan` stops. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.stops_before_timespan_stops(timespan_1)
            False
            >>> timespan_1.stops_before_timespan_stops(timespan_2)
            True
            >>> timespan_2.stops_before_timespan_stops(timespan_1)
            False
            >>> timespan_2.stops_before_timespan_stops(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_before_timespan_1_stops(timespan, self)

    def stops_during_timespan(self, timespan):
        '''True when timespan stops during `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.stops_during_timespan(timespan_1)
            True
            >>> timespan_1.stops_during_timespan(timespan_2)
            False
            >>> timespan_2.stops_during_timespan(timespan_1)
            False
            >>> timespan_2.stops_during_timespan(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_during_timespan_1(timespan, self)

    def stops_when_timespan_starts(self, timespan):
        '''True when timespan stops when `timespan` starts. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.stops_when_timespan_starts(timespan_1)
            False
            >>> timespan_1.stops_when_timespan_starts(timespan_2)
            True
            >>> timespan_2.stops_when_timespan_starts(timespan_1)
            False
            >>> timespan_2.stops_when_timespan_starts(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_when_timespan_1_starts(timespan, self)

    def stops_when_timespan_stops(self, timespan):
        '''True when timespan stops when `timespan` stops. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.stops_when_timespan_stops(timespan_1)
            True
            >>> timespan_1.stops_when_timespan_stops(timespan_2)
            False
            >>> timespan_2.stops_when_timespan_stops(timespan_1)
            False
            >>> timespan_2.stops_when_timespan_stops(timespan_2)
            True

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_when_timespan_1_stops(timespan, self)

    def stretch(self, multiplier, anchor=None):
        '''Stretch timespan by `multiplier` relative to `anchor`.

        Example 1. Stretch relative to timespan start offset:

            >>> timespantools.Timespan(3, 10).stretch(Multiplier(2))
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(17, 1))

        Example 2. Stretch relative to timespan stop offset:

            >>> timespantools.Timespan(3, 10).stretch(Multiplier(2), Offset(10))
            Timespan(start_offset=Offset(-4, 1), stop_offset=Offset(10, 1))

        Example 3: Stretch relative to offset prior to timespan:

            >>> timespantools.Timespan(3, 10).stretch(Multiplier(2), Offset(0))
            Timespan(start_offset=Offset(6, 1), stop_offset=Offset(20, 1))

        Example 4: Stretch relative to offset after timespan:

            >>> timespantools.Timespan(3, 10).stretch(Multiplier(3), Offset(12))
            Timespan(start_offset=Offset(-15, 1), stop_offset=Offset(6, 1))

        Example 5: Stretch relative to offset that happens during timespan:

            >>> timespantools.Timespan(3, 10).stretch(Multiplier(2), Offset(4))
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(16, 1))

        Return newly emitted timespan.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        assert 0 < multiplier
        if anchor is None:
            anchor = self.start_offset
        new_start_offset = (multiplier * (self.start_offset - anchor)) + anchor
        new_stop_offset =  (multiplier * (self.stop_offset - anchor)) + anchor
        return type(self)(new_start_offset, new_stop_offset)

    def translate(self, translation=None):
        '''Translate timespan by `translation`.

            >>> timespan = timespantools.Timespan(5, 10)

        ::

            >>> timespan.translate(2)
            Timespan(start_offset=Offset(7, 1), stop_offset=Offset(12, 1))

        Emit newly constructed timespan.
        '''
        return self.translate_offsets(translation, translation)

    def translate_offsets(self, start_offset_translation=None, stop_offset_translation=None):
        '''Translate timespan start offset by `start_offset_translation` and
        stop offset by `stop_offset_translation`::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2))

        ::

            >>> timespan.translate_offsets(start_offset_translation=Duration(-1, 8))
            Timespan(start_offset=Offset(3, 8), stop_offset=Offset(3, 2))

        Emit newly constructed timespan.
        '''
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = durationtools.Duration(start_offset_translation)
        stop_offset_translation = durationtools.Duration(stop_offset_translation)
        new_start_offset = self.start_offset + start_offset_translation
        new_stop_offset = self.stop_offset + stop_offset_translation
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    def trisects_timespan(self, timespan):
        '''True when timespan trisects `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 6)

        ::

            >>> timespan_1.trisects_timespan(timespan_1)
            False
            >>> timespan_1.trisects_timespan(timespan_2)
            False
            >>> timespan_2.trisects_timespan(timespan_1)
            True
            >>> timespan_2.trisects_timespan(timespan_2)
            False

        Return boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_trisects_timespan_1(timespan, self)
