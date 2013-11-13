# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from abjad.tools.mathtools.BoundedObject import BoundedObject


class Timespan(BoundedObject):
    r'''A closed-open interval.

    ..  container:: example

        **Example:**

        ::

                >>> timespan_1 = timespantools.Timespan(0, 10)
                >>> timespan_2 = timespantools.Timespan(5, 12)
                >>> timespan_3 = timespantools.Timespan(-2, 2)
                >>> timespan_4 = timespantools.Timespan(10, 20)

    Timespans are immutable and treated as value objects.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_offset',
        '_stop_offset',
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
        r'''Logical AND of two timespans:

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

        Returns timespan inventory.
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
        r'''True when `timespan` is a timespan with equal offsets:

        ::

            >>> timespantools.Timespan(1, 3) == timespantools.Timespan(1, 3)
            True

        Otherwise false:

        ::

            >>> timespantools.Timespan(1, 3) == timespantools.Timespan(2, 3)
            False

        Returns boolean.
        '''
        if isinstance(timespan, type(self)):
            return self.offsets == timespan.offsets
        return False

    def __format__(self, format_specification=''):
        r'''Formats timespan.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(timespan_1)
            timespantools.Timespan(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(10, 1)
                )

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return self._tools_package_qualified_indented_repr
        return str(self)

    def __ge__(self, expr):
        r'''True when `expr` start offset is greater or equal
        to timespan start offset:

        ::

            >>> timespan_2 >= timespan_3
            True

        Otherwise false:

        ::

            >>> timespan_1 >= timespan_2
            False

        Returns boolean.
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
        r'''True when `expr` start offset is greater than
        timespan start offset:

        ::

            >>> timespan_2 > timespan_3
            True

        Otherwise false:

        ::

            >>> timespan_1 > timespan_2
            False

        Returns boolean.
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
        r'''True when `expr` start offset is less than or equal to
        timespan start offset:

        ::

            >>> timespan_2 <= timespan_3
            False

        Otherwise false:

        ::

            >>> timespan_1 <= timespan_2
            True

        Returns boolean.
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
        r'''Defined equal to ``1`` for all timespans:

        ::

            >>> len(timespan_1)
            1

        Returns positive integer.
        '''
        return 1

    def __lt__(self, expr):
        r'''True when `expr` start offset is less than timespan start offset:

        ::

            >>> timespan_1 < timespan_2
            True

        Otherwise false:

        ::

            >>> timespan_2 < timespan_3
            False

        Returns boolean.
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
        r'''True when `timespan` is not a timespan with equivalent offsets:

        ::

            >>> timespantools.Timespan(1, 3) != timespantools.Timespan(2, 3)
            True

        Otherwise false:

        ::

            >>> timespantools.Timespan(1, 3) != timespantools.Timespan(2/2, (3, 1))
            False

        Returns boolean.
        '''
        return not self == timespan

    def __or__(self, expr):
        r'''Logical OR of two timespans:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 12)
            >>> timespan_3 = timespantools.Timespan(-2, 2)
            >>> timespan_4 = timespantools.Timespan(10, 20)

        ::

            >>> new_timespan = timespan_1 | timespan_2
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_1 | timespan_3
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                ])

        ::


            >>> new_timespan = timespan_1 | timespan_4
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_2 | timespan_3
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_2 | timespan_4
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_3 | timespan_4
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    ),
                ])

        Returns timespan inventory.
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
        r'''Interpreter representation of timespan:

        ::

            >>> timespan_1
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        Returns string.
        '''
        return BoundedObject.__repr__(self)

    def __sub__(self, expr):
        r'''Subtract `expr` from timespan:

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

        Returns timespan inventory.
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
        r'''Logical AND of two timespans:

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 12)
            >>> timespan_3 = timespantools.Timespan(-2, 2)
            >>> timespan_4 = timespantools.Timespan(10, 20)

        ::

            >>> new_timespan = timespan_1 ^ timespan_2
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(5, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_1 ^ timespan_3
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(0, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(2, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_1 ^ timespan_4
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_2 ^ timespan_3
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(12, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_2 ^ timespan_4
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(5, 1),
                    stop_offset=durationtools.Offset(10, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(12, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    ),
                ])

        ::

            >>> new_timespan = timespan_3 ^ timespan_4
            >>> print format(new_timespan)
            timespantools.TimespanInventory([
                timespantools.Timespan(
                    start_offset=durationtools.Offset(-2, 1),
                    stop_offset=durationtools.Offset(2, 1)
                    ),
                timespantools.Timespan(
                    start_offset=durationtools.Offset(10, 1),
                    stop_offset=durationtools.Offset(20, 1)
                    ),
                ])

        Returns timespan inventory.
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
            return self.intersects_timespan(expr) or \
                self.stops_when_timespan_starts(expr)
        return False

    def _get_timespan(self, expr):
        if isinstance(expr, Timespan):
            start_offset, stop_offset = expr.offsets
        elif hasattr(expr, '_get_timespan'):
            start_offset, stop_offset = expr._get_timespan().offsets
        # TODO: remove this branch in favor of the _get_timespan above
        elif hasattr(expr, 'get_timespan'):
            start_offset, stop_offset = expr.get_timespan().offsets
        else:
            start_offset, stop_offset = expr.timespan.offsets
        return type(self)(start_offset, stop_offset)

    def _implements_timespan_interface(self, timespan):
        if hasattr(timespan, 'start_offset') and \
            hasattr(timespan, 'stop_offset'):
            return True
        if hasattr(timespan, '_get_timespan'):
            return True
        # TODO: remove this branch in favor of the _get_timespan above
        if hasattr(timespan, 'get_timespan'):
            return True
        if hasattr(timespan, 'timespan'):
            return True
        return False

    def _initialize_offset(self, offset):
        if offset in (NegativeInfinity, Infinity):
            return offset
        else:
            return durationtools.Offset(offset)

    ### PUBLIC PROPERTIES ###

    @property
    def axis(self):
        r'''Arithmetic mean of timespan start- and stop-offsets:

        ::

            >>> timespan_1.axis
            Offset(5, 1)

        Returns offset.
        '''
        return (self.start_offset + self.stop_offset) / 2

    @property
    def duration(self):
        r'''Get timespan duration:

        ::

            >>> timespan_1.duration
            Duration(10, 1)

        Returns duration.
        '''
        return self.stop_offset - self.start_offset

    @property
    def is_closed(self):
        r'''False for all timespans:

        ::

            >>> timespan_1.is_closed
            False

        Returns boolean.
        '''
        return BoundedObject.is_closed.fget(self)

    @property
    def is_half_closed(self):
        r'''True for all timespans:

        ::

            >>> timespan_1.is_half_closed
            True

        Returns boolean.
        '''
        return BoundedObject.is_half_closed.fget(self)

    @property
    def is_half_open(self):
        r'''True for all timespans:

        ::

            >>> timespan_1.is_half_open
            True

        Returns boolean.
        '''
        return BoundedObject.is_half_open.fget(self)

    @property
    def is_left_closed(self):
        r'''True for all timespans.

            >>> timespan_1.is_left_closed
            True

        Returns boolean.
        '''
        return True


    @property
    def is_left_open(self):
        r'''False for all timespans.

            >>> timespan_1.is_left_open
            False

        Returns boolean.
        '''
        return False

    @property
    def is_open(self):
        r'''False for all timespans:

        ::

            >>> timespan_1.is_open
            False

        Returns boolean.
        '''
        return BoundedObject.is_open.fget(self)

    @property
    def is_right_closed(self):
        r'''False for all timespans.

            >>> timespan_1.is_right_closed
            False

        Returns boolean.
        '''
        return False


    @property
    def is_right_open(self):
        r'''True for all timespans.

            >>> timespan_1.is_right_open
            True

        Returns boolean.
        '''
        return True

    @property
    def is_well_formed(self):
        r'''True when timespan start offset preceeds timespan stop offset.
        Otherwise false:

        ::

            >>> timespan_1.is_well_formed
            True

        Returns boolean.
        '''
        return self.start_offset < self.stop_offset

    @property
    def offsets(self):
        r'''Timespan offsets:

        ::

            >>> timespan_1.offsets
            (Offset(0, 1), Offset(10, 1))

        Returns offset pair.
        '''
        return self.start_offset, self.stop_offset

    @property
    def start_offset(self):
        r'''Timespan start offset:

        ::

            >>> timespan_1.start_offset
            Offset(0, 1)

        Returns offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        r'''Timespan stop offset:

        ::

            >>> timespan_1.stop_offset
            Offset(10, 1)

        Returns offset.
        '''
        return self._stop_offset

    ### PUBLIC METHODS ###

    def contains_timespan_improperly(self, timespan):
        r'''True when timespan contains `timespan` improperly.
        Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_contains_timespan_1_improperly(
                timespan, self)

    def curtails_timespan(self, timespan):
        r'''True when timespan curtails `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_curtails_timespan_1(
                timespan, self)

    def delays_timespan(self, timespan):
        r'''True when timespan delays `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)
            >>> timespan_2 = timespantools.Timespan(5, 15)
            >>> timespan_3 = timespantools.Timespan(10, 20)

        ::

            >>> timespan_1.delays_timespan(timespan_2)
            True
            >>> timespan_2.delays_timespan(timespan_3)
            True

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_delays_timespan_1(
                timespan, self)

    def divide_by_ratio(self, ratio):
        r'''Divide timespan by `ratio`:

        ::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2))

        ::

            >>> for x in timespan.divide_by_ratio((1, 2, 1)):
            ...     x
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(3, 4))
            Timespan(start_offset=Offset(3, 4), stop_offset=Offset(5, 4))
            Timespan(start_offset=Offset(5, 4), stop_offset=Offset(3, 2))

        Returns tuple of newly constructed timespans.
        '''
        if isinstance(ratio, int):
            ratio = ratio * (1, )
        ratio = mathtools.Ratio(ratio)
        unit_duration = self.duration / sum(ratio)
        part_durations = [numerator * unit_duration for numerator in ratio]
        start_offsets = mathtools.cumulative_sums(
            [self.start_offset] + part_durations,
            start=None,
            )
        offset_pairs = sequencetools.iterate_sequence_pairwise_strict(
            start_offsets)
        result = [type(self)(*offset_pair) for offset_pair in offset_pairs]
        return tuple(result)

    def get_overlap_with_timespan(self, timespan):
        '''Get duration of overlap with `timespan`:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 15)
            >>> timespan_2 = timespantools.Timespan(5, 10)
            >>> timespan_3 = timespantools.Timespan(6, 6)
            >>> timespan_4 = timespantools.Timespan(12, 22)


        ::

            >>> timespan_1.get_overlap_with_timespan(timespan_1)
            Duration(15, 1)

        ::

            >>> timespan_1.get_overlap_with_timespan(timespan_2)
            Duration(5, 1)

        ::

            >>> timespan_1.get_overlap_with_timespan(timespan_3)
            Duration(0, 1)

        ::

            >>> timespan_1.get_overlap_with_timespan(timespan_4)
            Duration(3, 1)

        ::

            >>> timespan_2.get_overlap_with_timespan(timespan_2)
            Duration(5, 1)

        ::

            >>> timespan_2.get_overlap_with_timespan(timespan_3)
            Duration(0, 1)

        ::

            >>> timespan_2.get_overlap_with_timespan(timespan_4)
            Duration(0, 1)

        ::

            >>> timespan_3.get_overlap_with_timespan(timespan_3)
            Duration(0, 1)

        ::

            >>> timespan_3.get_overlap_with_timespan(timespan_4)
            Duration(0, 1)

        ::

            >>> timespan_4.get_overlap_with_timespan(timespan_4)
            Duration(10, 1)


        Returns duration.
        '''
        if self._implements_timespan_interface(timespan):
            result = durationtools.Duration(
                sum(x.duration for x in self & timespan))
            return result

    def happens_during_timespan(self, timespan):
        r'''True when timespan happens during `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_happens_during_timespan_1(
                timespan, self)

    def intersects_timespan(self, timespan):
        r'''True when timespan intersects `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_intersects_timespan_1(
                timespan, self)

    def is_congruent_to_timespan(self, timespan):
        r'''True when timespan is congruent to `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_is_congruent_to_timespan_1(
                timespan, self)

    def is_tangent_to_timespan(self, timespan):
        r'''True when timespan is tangent to `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if hasattr(timespan, 'start_offset'):
            if self.stop_offset == timespan.start_offset:
                return True
        if hasattr(timespan, 'stop_offset'):
            if timespan.stop_offset == self.start_offset:
                return True
        return False

    def new(self, **kwargs):
        r'''Create new timespan with `kwargs`:

        ::

            >>> timespan_1.new(stop_offset=Offset(9))
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 1))

        Returns new timespan.
        '''
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_dictionary = \
            manager.get_keyword_argument_dictionary(self)
        positional_argument_dictionary = \
            manager.get_positional_argument_dictionary(self)
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        positional_argument_names = getattr(
            self, '_positional_argument_names', None) or \
            manager.get_positional_argument_names(self)
        for positional_argument_name in positional_argument_names:
            positional_argument_value = positional_argument_dictionary[
                positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(self)(
            *positional_argument_values, **keyword_argument_dictionary)
        return result

    def overlaps_all_of_timespan(self, timespan):
        r'''True when timespan overlaps all of `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_all_of_timespan_1(
                timespan, self)

    def overlaps_only_start_of_timespan(self, timespan):
        r'''True when timespan overlaps only start of `timespan`.
        Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_only_start_of_timespan_1(
                timespan, self)

    def overlaps_only_stop_of_timespan(self, timespan):
        r'''True when timespan overlaps only stop of `timespan`.
        Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_only_stop_of_timespan_1(
                timespan, self)

    def overlaps_start_of_timespan(self, timespan):
        r'''True when timespan overlaps start of `timespan`.
        Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_start_of_timespan_1(
                timespan, self)

    def overlaps_stop_of_timespan(self, timespan):
        r'''True when timespan overlaps start of `timespan`.
        Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_overlaps_stop_of_timespan_1(
                timespan, self)

    def reflect(self, axis=None):
        r'''Reverse timespan about `axis`.

        ..  container:: example

            **Example 1.** Reverse timespan about timespan axis:

            ::

                >>> timespantools.Timespan(3, 6).reflect()
                Timespan(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        ..  container:: example

            **Example 2.** Reverse timespan about arbitrary axis:

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

    def round_offsets(self, multiplier, anchor=Left, must_be_well_formed=True):
        '''Round timespan offsets to multiple of `multiplier`:

        ::

            >>> timespan = timespantools.Timespan((1, 5), (4, 5))

        ::

            >>> timespan.round_offsets(1)
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(1, 1))

        ::

            >>> timespan.round_offsets(2)
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(2, 1))

        ::

            >>> timespan.round_offsets(
            ...     2,
            ...     anchor=Right,
            ...     )
            Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(0, 1))

        ::

            >>> timespan.round_offsets(
            ...     2,
            ...     anchor=Right,
            ...     must_be_well_formed=False,
            ...     )
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(0, 1))

        Emit newly constructed timespan.
        '''
        multiplier = abs(durationtools.Multiplier(multiplier))
        assert 0 < multiplier
        new_start_offset = durationtools.Offset(
            int(round(self.start_offset / multiplier)) * multiplier)
        new_stop_offset = durationtools.Offset(
            int(round(self.stop_offset / multiplier)) * multiplier)
        if (new_start_offset == new_stop_offset) and must_be_well_formed:
            if anchor is Left:
                new_stop_offset = new_stop_offset + multiplier
            else:
                new_start_offset = new_start_offset - multiplier
        return self.new(
            start_offset=new_start_offset,
            stop_offset=new_stop_offset,
            )

    def scale(self, multiplier, anchor=Left):
        r'''Scale timespan by `multiplier`.

            >>> timespan = timespantools.Timespan(3, 6)

        ..  container:: example

            **Example 1.** Scale timespan relative to timespan start offset:

            ::

                >>> timespan.scale(Multiplier(2))
                Timespan(start_offset=Offset(3, 1), stop_offset=Offset(9, 1))

        ..  container:: example

            **Example 2.** Scale timespan relative to timespan stop offset:

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
        r'''Set timespan duration to `duration`:

        ::

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
        r'''Set timespan start offset to `start_offset` and
        stop offset to `stop_offset`:

        ::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2))

        ::

            >>> timespan.set_offsets(stop_offset=Offset(7, 8))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(7, 8))

        Subtract negative `start_offset` from existing stop offset:

        ::

            >>> timespan.set_offsets(start_offset=Offset(-1, 2))
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 2))

        Subtract negative `stop_offset` from existing stop offset:

        ::

            >>> timespan.set_offsets(stop_offset=Offset(-1, 2))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(1, 1))

        Emit newly constructed timespan.
        '''
        if start_offset is not None and 0 <= start_offset:
            new_start_offset = start_offset
        elif start_offset is not None and start_offset < 0:
            new_start_offset = \
                self.stop_offset + durationtools.Offset(start_offset)
        else:
            new_start_offset = self.start_offset
        if stop_offset is not None and 0 <= stop_offset:
            new_stop_offset = stop_offset
        elif stop_offset is not None and stop_offset < 0:
            new_stop_offset = \
                self.stop_offset + durationtools.Offset(stop_offset)
        else:
            new_stop_offset = self.stop_offset
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    # TODO: extend to self.split_at_offsets()
    def split_at_offset(self, offset):
        r'''Split into two parts when `offset` happens during timespan:

        ::

            >>> timespan = timespantools.Timespan(0, 5)

        ::

            >>> left, right = timespan.split_at_offset(Offset(2))

        ::

            >>> left
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(2, 1))

        ::

            >>> right
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(5, 1))

        Otherwise return a copy of timespan:

        ::

            >>> timespan.split_at_offset(Offset(12))
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(5, 1))

        Returns one or two newly constructed timespans.
        '''
        offset = durationtools.Offset(offset)
        if self.start_offset < offset < self.stop_offset:
            left = type(self)(self.start_offset, offset)
            right = type(self)(offset, self.stop_offset)
            return left, right
        else:
            return type(self)(self.start_offset, self.stop_offset)

    def starts_after_offset(self, offset):
        r'''True when timespan overlaps start of `timespan`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_after_offset(Offset(-5))
            True
            >>> timespan_1.starts_after_offset(Offset(0))
            False
            >>> timespan_1.starts_after_offset(Offset(5))
            False

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return offset < self.start_offset

    def starts_after_timespan_starts(self, timespan):
        r'''True when timespan starts after `timespan` starts. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_after_timespan_1_starts(
                timespan, self)

    def starts_after_timespan_stops(self, timespan):
        r'''True when timespan starts after `timespan` stops. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_after_timespan_1_stops(
                timespan, self)

    def starts_at_offset(self, offset):
        r'''True when timespan starts at `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_at_offset(Offset(-5))
            False
            >>> timespan_1.starts_at_offset(Offset(0))
            True
            >>> timespan_1.starts_at_offset(Offset(5))
            False

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.start_offset == offset

    def starts_at_or_after_offset(self, offset):
        r'''True when timespan starts at or after `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_at_or_after_offset(Offset(-5))
            True
            >>> timespan_1.starts_at_or_after_offset(Offset(0))
            True
            >>> timespan_1.starts_at_or_after_offset(Offset(5))
            False

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return offset <= self.start_offset

    def starts_before_offset(self, offset):
        r'''True when timespan starts before `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_before_offset(Offset(-5))
            False
            >>> timespan_1.starts_before_offset(Offset(0))
            False
            >>> timespan_1.starts_before_offset(Offset(5))
            True

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.start_offset < offset

    def starts_before_or_at_offset(self, offset):
        r'''True when timespan starts before or at `offset`.
        Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_before_or_at_offset(Offset(-5))
            False
            >>> timespan_1.starts_before_or_at_offset(Offset(0))
            True
            >>> timespan_1.starts_before_or_at_offset(Offset(5))
            True

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.start_offset <= offset

    def starts_before_timespan_starts(self, timespan):
        r'''True when timespan starts before `timespan` starts.
        Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_before_timespan_1_starts(
                timespan, self)

    def starts_before_timespan_stops(self, timespan):
        r'''True when timespan starts before `timespan` stops. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_before_timespan_1_stops(
                timespan, self)

    def starts_during_timespan(self, timespan):
        r'''True when timespan starts during `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_during_timespan_1(
                timespan, self)

    def starts_when_timespan_starts(self, timespan):
        r'''True when timespan starts when `timespan` starts. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_when_timespan_1_starts(
                timespan, self)

    def starts_when_timespan_stops(self, timespan):
        r'''True when timespan starts when `timespan` stops. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_starts_when_timespan_1_stops(
                timespan, self)

    def stops_after_offset(self, offset):
        r'''True when timespan stops after `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.starts_after_offset(Offset(-5))
            True
            >>> timespan_1.starts_after_offset(Offset(0))
            False
            >>> timespan_1.starts_after_offset(Offset(5))
            False

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return offset < self.stop_offset

    def stops_after_timespan_starts(self, timespan):
        r'''True when timespan stops when `timespan` starts. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_after_timespan_1_starts(
                timespan, self)

    def stops_after_timespan_stops(self, timespan):
        r'''True when timespan stops when `timespan` stops. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_after_timespan_1_stops(
                timespan, self)

    def stops_at_offset(self, offset):
        r'''True when timespan stops at `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.stops_at_offset(Offset(-5))
            False
            >>> timespan_1.stops_at_offset(Offset(0))
            False
            >>> timespan_1.stops_at_offset(Offset(5))
            False

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.stop_offset == offset

    def stops_at_or_after_offset(self, offset):
        r'''True when timespan stops at or after `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.stops_at_or_after_offset(Offset(-5))
            True
            >>> timespan_1.stops_at_or_after_offset(Offset(0))
            True
            >>> timespan_1.stops_at_or_after_offset(Offset(5))
            True

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return offset <= self.stop_offset

    def stops_before_offset(self, offset):
        r'''True when timespan stops before `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.stops_before_offset(Offset(-5))
            False
            >>> timespan_1.stops_before_offset(Offset(0))
            False
            >>> timespan_1.stops_before_offset(Offset(5))
            False

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.stop_offset < offset

    def stops_before_or_at_offset(self, offset):
        r'''True when timespan stops before or at `offset`. Otherwise false:

        ::

            >>> timespan_1 = timespantools.Timespan(0, 10)

        ::

            >>> timespan_1.stops_before_or_at_offset(Offset(-5))
            False
            >>> timespan_1.stops_before_or_at_offset(Offset(0))
            False
            >>> timespan_1.stops_before_or_at_offset(Offset(5))
            False

        Returns boolean.
        '''
        offset = durationtools.Offset(offset)
        return self.stop_offset <= offset

    def stops_before_timespan_starts(self, timespan):
        r'''True when timespan stops before `timespan` starts.
        Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_before_timespan_1_starts(
                timespan, self)

    def stops_before_timespan_stops(self, timespan):
        r'''True when timespan stops before `timespan` stops. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_before_timespan_1_stops(
                timespan, self)

    def stops_during_timespan(self, timespan):
        r'''True when timespan stops during `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_during_timespan_1(
                timespan, self)

    def stops_when_timespan_starts(self, timespan):
        r'''True when timespan stops when `timespan` starts. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_when_timespan_1_starts(
                timespan, self)

    def stops_when_timespan_stops(self, timespan):
        r'''True when timespan stops when `timespan` stops. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_stops_when_timespan_1_stops(
                timespan, self)

    def stretch(self, multiplier, anchor=None):
        r'''Stretch timespan by `multiplier` relative to `anchor`.

        .. container:: example

            **Example 1.** Stretch relative to timespan start offset:

            ::

                >>> timespantools.Timespan(3, 10).stretch(Multiplier(2))
                Timespan(start_offset=Offset(3, 1), stop_offset=Offset(17, 1))

        .. container:: example

            **Example 2.** Stretch relative to timespan stop offset:

            ::

                >>> timespantools.Timespan(3, 10).stretch(Multiplier(2), Offset(10))
                Timespan(start_offset=Offset(-4, 1), stop_offset=Offset(10, 1))

        .. container:: example

            **Example 3.** Stretch relative to offset prior to timespan:

            ::

                >>> timespantools.Timespan(3, 10).stretch(Multiplier(2), Offset(0))
                Timespan(start_offset=Offset(6, 1), stop_offset=Offset(20, 1))

        .. container:: example

            **Example 4.** Stretch relative to offset after timespan:

            ::

                >>> timespantools.Timespan(3, 10).stretch(Multiplier(3), Offset(12))
                Timespan(start_offset=Offset(-15, 1), stop_offset=Offset(6, 1))

        .. container:: example

            **Example 5.** Stretch relative to offset that happens during timespan:

            ::

                >>> timespantools.Timespan(3, 10).stretch(Multiplier(2), Offset(4))
                Timespan(start_offset=Offset(2, 1), stop_offset=Offset(16, 1))

        Returns newly emitted timespan.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        assert 0 < multiplier
        if anchor is None:
            anchor = self.start_offset
        new_start_offset = (multiplier * (self.start_offset - anchor)) + anchor
        new_stop_offset =  (multiplier * (self.stop_offset - anchor)) + anchor
        return type(self)(new_start_offset, new_stop_offset)

    def translate(self, translation=None):
        r'''Translate timespan by `translation`.

            >>> timespan = timespantools.Timespan(5, 10)

        ::

            >>> timespan.translate(2)
            Timespan(start_offset=Offset(7, 1), stop_offset=Offset(12, 1))

        Emit newly constructed timespan.
        '''
        return self.translate_offsets(translation, translation)

    def translate_offsets(
        self,
        start_offset_translation=None,
        stop_offset_translation=None,
        ):
        r'''Translate timespan start offset by `start_offset_translation` and
        stop offset by `stop_offset_translation`:

        ::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2))

        ::

            >>> timespan.translate_offsets(
            ...     start_offset_translation=Duration(-1, 8))
            Timespan(start_offset=Offset(3, 8), stop_offset=Offset(3, 2))

        Emit newly constructed timespan.
        '''
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = \
            durationtools.Duration(start_offset_translation)
        stop_offset_translation = \
            durationtools.Duration(stop_offset_translation)
        new_start_offset = self.start_offset + start_offset_translation
        new_stop_offset = self.stop_offset + stop_offset_translation
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    def trisects_timespan(self, timespan):
        r'''True when timespan trisects `timespan`. Otherwise false:

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

        Returns boolean.
        '''
        if self._implements_timespan_interface(timespan):
            return timerelationtools.timespan_2_trisects_timespan_1(
                timespan, self)
