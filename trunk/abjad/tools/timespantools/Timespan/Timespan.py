from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from abjad.tools.mathtools.BoundedObject import BoundedObject


class Timespan(BoundedObject):
    r'''.. versionadded:: 2.11

    Timespan ``[1/2, 3/2)``::

        >>> timespan = timespantools.Timespan((1, 2), (3, 2)) 

    ::

        >>> timespan
        Timespan(start_offset=Offset(1, 2), stop_offset=Offset(3, 2))

    ::
    
        >>> z(timespan)
        timespantools.Timespan(
            start_offset=durationtools.Offset(1, 2),
            stop_offset=durationtools.Offset(3, 2)
            )

    Timespans are object-modeled offset pairs.

    Timespans are immutable and treated as value objects.
    '''

    ### INITIALIZER ###

    def __init__(self, start_offset=None, stop_offset=None):
        BoundedObject.__init__(self)
        start_offset = self._initialize_offset(start_offset)
        stop_offset = self._initialize_offset(stop_offset)
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when `expr` is a timespan with equivalent offsets::

            >>> timespantools.Timespan(1, 3) == timespantools.Timespan(2/2, (3, 1))
            True

        Otherwise false::

            >>> timespantools.Timespan(1, 3) == timespantools.Timespan(2, 3)
            False

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            return self.offsets == expr.offsets
        return False

    def __ne__(self, expr):
        '''True when `expr` is not a timespan with equivalent offsets::

            >>> timespantools.Timespan(1, 3) != timespantools.Timespan(2, 3)
            True

        Otherwise false::

            >>> timespantools.Timespan(1, 3) != timespantools.Timespan(2/2, (3, 1))
            False

        Return boolean.
        '''
        return not self == expr

    ### PRIVATE METHODS ###

    def _initialize_offset(self, offset):
        if offset is not None:
            return durationtools.Offset(offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        '''Get timespan duration::

            >>> timespan.duration
            Duration(1, 1)

        Return duration.
        '''
        return self.stop_offset - self.start_offset

    @property
    def is_well_formed(self):
        '''True when timespan start offset preceeds timespan stop offset.
        Otherwise false.

            >>> timespan.is_well_formed
            True

        Return boolean.
        '''
        return self.start_offset < self.stop_offset

    @property
    def offsets(self):
        '''Timespan offsets::

            >>> timespan.offsets
            (Offset(1, 2), Offset(3, 2))

        Return offset pair.
        '''
        return self.start_offset, self.stop_offset

    @property
    def start_offset(self):
        '''Timespan start offset::

            >>> timespan.start_offset
            Offset(1, 2)

        Return offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Timespan stop offset::

            >>> timespan.stop_offset
            Offset(3, 2)
            
        Return offset.
        '''
        return self._stop_offset

    ### PUBLIC METHODS ###

    def contains_expr_improperly(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_contains_timespan_1_improperly(expr, self)

    def curtails_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_curtails_timespan_1(expr, self)

    def delays_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_delays_timespan_1(expr, self)

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

    def fuse(self, expr):
        '''Fuse if timespan stops when `expr` starts::

            >>> timespan_1 = timespantools.Timespan(0, 5)
            >>> timespan_2 = timespantools.Timespan(5, 10)

        ::

            >>> timespan_1.fuse(timespan_2)
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        Raise exception when timespan does not stop when `expr` starts.

        Return newly created timespan.
        '''
        assert isinstance(expr, type(self)), repr(expr)
        assert self.stops_when_expr_starts(expr), repr(expr)
        return type(self)(self.start_offset, expr.stop_offset)

    def happens_during_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_happens_during_timespan_1(expr, self)

    def intersects_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_intersects_timespan_1(expr, self)

    def is_congruent_to_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_is_congruent_to_timespan_1(expr, self)

    def is_tangent_to_expr(self, expr):
        '''True when `expr` has offsets
        and `self.stop_offset` equals `expr.start_offset`::

            >>> timespan_1 = timespantools.Timespan(5, 10)
            >>> timespan_2 = timespantools.Timespan(10, 15)

        ::

            >>> timespan_1.is_tangent_to_expr(timespan_2)
            True

        Or when `expr.stop_offset` equals `self.start_offset`::

            >>> timespan_2.is_tangent_to_expr(timespan_1)
            True    

        Otherwise false::

            >>> timespan_1.is_tangent_to_expr('text')
            False

        Return boolean.
        '''
        if hasattr(expr, 'start_offset'):
            if self.stop_offset == expr.start_offset:
                return True
        if hasattr(expr, 'stop_offset'):
            if expr.stop_offset == self.start_offset:
                return True
        return False

    def overlaps_all_of_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_overlaps_all_of_timespan_1(expr, self)

    def overlaps_only_start_of_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_overlaps_only_start_of_timespan_1(expr, self)

    def overlaps_only_stop_of_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_overlaps_only_stop_of_timespan_1(expr, self)

    def overlaps_start_of_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_overlaps_start_of_timespan_1(expr, self)

    def overlaps_stop_of_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_overlaps_stop_of_timespan_1(expr, self)

    def scale(self, multiplier):
        '''Scale timespan by `multiplier`::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2)) 

        ::

            >>> timespan.scale(Multiplier(1, 2))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(1, 1))

        Return newly constructed timespan.
        '''
        multiplier = durationtools.Multiplier(multiplier)
        new_start_offset = self.start_offset
        new_duration = multiplier * self.duration
        new_stop_offset = self.start_offset + new_duration
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    def set_duration(self, duration):
        '''Set timespan duration to `duration`::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2)) 

        ::

            >>> timespan.set_duration(Duration(3, 5))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(11, 10))

        Return newly constructed timespan.
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

        Return newly constructed timespan.
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

    def starts_after_expr_starts(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_starts_after_timespan_1_starts(expr, self)

    def starts_after_expr_stops(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_starts_after_timespan_1_stops(expr, self)

    def starts_before_expr_starts(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_starts_before_timespan_1_starts(expr, self)

    def starts_before_expr_stops(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_starts_before_timespan_1_stops(expr, self)

    def starts_during_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_starts_during_timespan_1(expr, self)

    def starts_when_expr_starts(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_starts_when_timespan_1_starts(expr, self)

    def starts_when_expr_stops(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_starts_when_timespan_1_stops(expr, self)

    def stops_after_expr_starts(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_stops_after_timespan_1_starts(expr, self)

    def stops_after_expr_stops(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_stops_after_timespan_1_stops(expr, self)

    def stops_before_expr_starts(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_stops_before_timespan_1_starts(expr, self)

    def stops_before_expr_stops(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_stops_before_timespan_1_stops(expr, self)

    def stops_during_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_stops_during_timespan_1(expr, self)

    def stops_when_expr_starts(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_stops_when_timespan_1_starts(expr, self)

    def stops_when_expr_stops(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_stops_when_timespan_1_stops(expr, self)

    def translate_offsets(self, start_offset_translation=None, stop_offset_translation=None):
        '''Translate timespan start offset by `start_offset_translation` and
        stop offset by `stop_offset_translation`::

            >>> timespan = timespantools.Timespan((1, 2), (3, 2)) 

        ::

            >>> timespan.translate_offsets(start_offset_translation=Duration(-1, 8))
            Timespan(start_offset=Offset(3, 8), stop_offset=Offset(3, 2))

        Return newly constructed timespan.
        '''
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = durationtools.Duration(start_offset_translation)
        stop_offset_translation = durationtools.Duration(stop_offset_translation)
        new_start_offset = self.start_offset + start_offset_translation
        new_stop_offset = self.stop_offset + stop_offset_translation
        result = type(self)(new_start_offset, new_stop_offset)
        return result

    def trisects_expr(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return timerelationtools.timespan_2_trisects_timespan_1(expr, self)
