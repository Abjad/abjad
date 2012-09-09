import abc
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import timespaninequalitytools 


class Command(AbjadObject):
    '''.. versionadded:: 1.0

    Abstract command class from which concrete command classes inherit.

    Basically a fancy tuple.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIAILIZER ###

    @abc.abstractmethod
    def __init__(self, resolved_value, start_segment_name, context_name, start_offset, stop_offset, duration):
        duration = durationtools.Duration(duration)
        assert isinstance(start_segment_name, str)
        start_offset = durationtools.Offset(start_offset)
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset - start_offset == duration, repr((stop_offset, start_offset, duration))
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        self._resolved_value = resolved_value
        self._duration = duration
        self._start_segment_name = start_segment_name
        self._start_offset = start_offset
        self._stop_offset = stop_offset
        self._context_name = context_name

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            for my_value, expr_value in zip(self._mandatory_argument_values, expr._mandatory_argument_values):
                if not my_value == expr_value:
                    return False
            else:
                return True
        return False

    def __lt__(self, expr):
        return self.starts_before(expr)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Name of context giving rise to command.
        '''
        return self._context_name

    @property
    def duration(self):
        return self._duration

    @property
    def resolved_value(self):
        return self._resolved_value

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def start_segment_name(self):
        return self._start_segment_name

    @property
    def stop_offset(self):
        return self._stop_offset

    @property
    def vector(self):
        return self._mandatory_argument_values

    ### PUBLIC METHODS ###

    def curtails(self, timespan_1):
        return timespan_1.start_offset < self.start_offset <= timespan_1.stop_offset <= self.stop_offset
        #return timespaninequalitytools.timespan_2_curtails_timespan_1(timespan_1, self)

    def delays(self, timespan_1):
        return self.start_offset <= timespan_1.start_offset < self.stop_offset
        #return timespaninequalitytools.timespan_2_delays_timespan_1(timespan_1, self)

    def equals(self, timespan_1):
        return self.starts_with(timespan_1) and self.stops_with(timespan_1)
        #return timespaninequalitytools.timespan_2_is_congruent_to_timespan_1(timespan_1, self)

    def improperly_contains(self, timespan_1):
        return self.starts_before_or_with(timespan_1) and timespan_1.stops_before_or_with(self)        
        #return timespaninequalitytools.timespan_2_contains_timespan_1_improperly(timespan_1, self)

    def overlaps_start_of(self, timespan_1):
        return self.start_offset < timespan_1.start_offset < self.stop_offset
        #return timespaninequalitytools.timespan_2_overlaps_start_of_timespan_1(timespan_1, self)

    def overlaps_stop_of(self, timespan_1):
        return self.start_offset < timespan_1.stop_offset < self.stop_offset 
        #return timespaninequalitytools.timespan_2_overlaps_stop_of_timespan_1(timespan_1, self)

    def properly_contains(self, timespan_1):
        return self.starts_before(timespan_1) and timespan_1.stops_before(self)
        #return timespaninequalitytools.timespan_2_trisects_timespan_1(self, timespan_1)

    def starts_before(self, timespan_1):
        return self.start_offset < timespan_1.start_offset
        #return timespaninequalitytools.timespan_2_starts_before_timespan_1_starts(timespan_1, self)

    def starts_before_or_with(self, timespan_1):
        return self.start_offset <= timespan_1.start_offset
        #return self.starts_before(timespan_1) or self.starts_with(timespan_1)

    def starts_with(self, timespan_1):
        return self.start_offset == timespan_1.start_offset
        #return timespaninequalitytools.timespan_2_starts_when_timespan_1_starts(timespan_1, self)

    def stops_before(self, timespan_1):
        return self.stop_offset < timespan_1.stop_offset
        #return timespaninequalitytools.timespan_2_stops_before_timespan_1_stops(timespan_1, self)

    def stops_before_or_with(self, timespan_1):
        return self.stop_offset <= timespan_1.stop_offset
        #return self.stops_before(timespan_1) or self.stops_with(timespan_1)

    def stops_with(self, timespan_1):
        return self.stop_offset == timespan_1.stop_offset
        #return timespaninequalitytools.timespan_2_stops_when_timespan_1_stops(timespan_1, self)
