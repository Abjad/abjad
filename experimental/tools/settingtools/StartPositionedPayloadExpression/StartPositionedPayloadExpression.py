import copy
import numbers
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.settingtools.Flamingo import Flamingo


class StartPositionedPayloadExpression(Flamingo):
    r'''Voiced, start-positioned product.
    ''' 

    ### INITIALIZER ###

    def __init__(self, payload=None, voice_name=None, start_offset=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        Flamingo.__init__(self, payload=payload, start_offset=start_offset)
        self._voice_name = voice_name

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Keep intersection of `timespan` and region product.

        Operate in place and return timespan inventory.
        '''
        if timespan.contains_timespan_improperly(self):
            result = timespantools.TimespanInventory([self]) 
        elif timespan.delays_timespan(self):
            split_offset = durationtools.Offset(timespan.stop_offset)
            duration_to_keep = split_offset - self.start_offset
            result = self._split_payload_at_offsets([duration_to_keep])
            trimmed_payload = result[0]
            self._payload = trimmed_payload
            result = timespantools.TimespanInventory([self])
        elif timespan.curtails_timespan(self):
            split_offset = durationtools.Offset(timespan.start_offset)
            duration_to_trim = split_offset - self.start_offset
            result = self._split_payload_at_offsets([duration_to_trim])
            trimmed_payload = result[-1]
            self._payload = trimmed_payload
            self._start_offset = split_offset
            result = timespantools.TimespanInventory([self])
        elif timespan.trisects_timespan(self):
            split_offsets = []
            split_offsets.append(timespan.start_offset - self.start_offset)
            split_offsets.append(timespan.duration)
            result = self._split_payload_at_offsets(split_offsets)
            middle_payload = result[1]
            middle_timespan = timespantools.Timespan(*timespan.offsets)
            middle_product = type(self)(
                payload=[], voice_name=self.voice_name, start_offset=middle_timespan.start_offset)
            middle_product._payload = middle_payload
            result = timespantools.TimespanInventory([middle_product])
        else:
            result = timespantools.TimespanInventory()
        return result

    def __len__(self):
        '''Defined equal to length of payload.

        Return nonnegative integer.
        '''
        return len(self.payload)

    def __lt__(self, expr):        
        '''True when rhythm region product starts before `expr`.

        Also true when rhythm region product starts when `expr` starts
        but rhythm region product stops before `expr` stops.

        Otherwise false.

        Return boolean.
        '''
        if self.timespan.starts_before_timespan_starts(expr):
            return True
        elif self.timespan.starts_when_timespan_starts(expr):
            return self.timespan.stops_before_timespan_stops(expr)
        return False

    def __or__(self, expr):
        '''Logical OR of two region products.

        Region products must be able to fuse.
        
        Return timespan inventory.
        '''
        assert self._can_fuse(expr)
        payload = self.payload + expr.payload
        result = type(self)([], voice_name=self.voice_name, start_offset=self.timespan.start_offset)
        result._payload = payload
        return timespantools.TimespanInventory([result])

    def __sub__(self, timespan):
        '''Subtract `timespan` from region product.

        Operate in place and return timespan inventory.
        '''
        if timespan.delays_timespan(self):
            split_offset = durationtools.Offset(timespan.stop_offset)
            duration_to_trim = split_offset - self.start_offset
            result = self._split_payload_at_offsets([duration_to_trim])
            trimmed_payload = result[-1]
            self._payload = trimmed_payload
            self._start_offset = split_offset
            result = timespantools.TimespanInventory([self])
        elif timespan.curtails_timespan(self):
            split_offset = durationtools.Offset(timespan.start_offset)
            duration_to_trim = self.stop_offset - split_offset
            if hasattr(self.payload, 'prolated_duration'):
                payload_duration = self.payload.prolated_duration
            else:
                payload_duration = self.payload.duration
            duration_to_keep = payload_duration - duration_to_trim
            result = self._split_payload_at_offsets([duration_to_keep])
            trimmed_payload = result[0]
            self._payload = trimmed_payload
            result = timespantools.TimespanInventory([self])
        elif timespan.trisects_timespan(self):
            split_offsets = []
            split_offsets.append(timespan.start_offset - self.start_offset)
            split_offsets.append(timespan.duration)
            result = self._split_payload_at_offsets(split_offsets)
            left_payload = result[0]
            right_payload = result[-1]
            left_timespan = timespantools.Timespan(self.start_offset)
            left_product = type(self)(
                payload=[], voice_name=self.voice_name, start_offset=left_timespan.start_offset)
            left_product._payload = left_payload
            right_timespan = timespantools.Timespan(timespan.stop_offset)
            right_product = type(self)(
                payload=[], voice_name=self.voice_name, start_offset=right_timespan.start_offset)
            right_product._payload = right_payload
            products = [left_product, right_product]
            result = timespantools.TimespanInventory(products)
        else:
            result = timespantools.TimespanInventory([self])
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _duration(self):
        if hasattr(self.payload, 'duration'):
            return self.payload.duration
        else:
            return self._get_duration_of_list(self.payload)

    @property
    def _payload_elements(self):
        return self.payload

    @property
    def _stop_offset(self):
        return self.start_offset + self._duration

    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        if isinstance(expr, type(self)):
            if self.timespan.stops_when_timespan_starts(expr):
                return self.voice_name == expr.voice_name
        return False

    def _get_duration_of_expr(self, expr):
        if hasattr(expr, 'duration'):
            return expr.duration
        elif hasattr(expr, 'prolated_duration'):
            return expr.prolated_duration
        elif isinstance(expr, numbers.Number):
            return durationtools.Duration(expr)
        else:
            return durationtools.Duration(expr)

    def _get_duration_of_list(self, expr):
        duration = durationtools.Duration(0)
        for element in expr:
            duration += self._get_duration_of_expr(element)
        return duration

#    @abc.abstractmethod
#    def _split_payload_at_offsets(self, offsets):
#        pass
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        '''Region product payload.
        '''
        return self._payload

    @property
    def stop_offset(self):
        '''Region product stop offset.

        Return offset.
        '''
        return self.timespan.stop_offset

    @property
    def timespan(self):
        '''Region product timespan.

        Return timespan.
        '''
        return timespantools.Timespan(self.start_offset, self._stop_offset)

    @property
    def voice_name(self):
        '''Region product voice name.

        Return string.
        '''
        return self._voice_name

    ### PUBLIC METHODS ###
    
    def new(self, **kwargs):
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

    def partition_by_ratio(self, ratio):
        '''Partition region product payload by ratio.

        Operate in place and return newly constructed inventory.
        '''
        from experimental.tools import settingtools
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(self._payload_elements, ratio)
        durations = [self._get_duration_of_list(part) for part in parts]
        payload_parts = self._split_payload_at_offsets(durations)
        start_offsets = mathtools.cumulative_sums_zero(durations)[:-1]
        start_offsets = [self.start_offset + start_offset for start_offset in start_offsets]
        products = settingtools.RegionExpressionInventory()
        for payload_part, start_offset in zip(payload_parts, start_offsets):
            timespan = timespantools.Timespan(start_offset)
            product = type(self)([], self.voice_name, timespan.start_offset)
            product._payload = payload_part
            products.append(product)
        return products

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition region product payload by ratio of durations.

        Operate in place and return newly constructed inventory.
        '''
        from experimental.tools import settingtools
        element_durations = [self._get_duration_of_expr(leaf) for leaf in self._payload_elements]
        integers = durationtools.durations_to_integers(element_durations)
        parts = sequencetools.partition_sequence_by_ratio_of_weights(integers, ratio)
        part_lengths = [len(part) for part in parts]
        parts = sequencetools.partition_sequence_by_counts(self._payload_elements, part_lengths)
        durations = [self._get_duration_of_list(part) for part in parts]
        payload_parts = self._split_payload_at_offsets(durations)
        start_offsets = mathtools.cumulative_sums_zero(durations)[:-1]
        start_offsets = [self.start_offset + start_offset for start_offset in start_offsets]
        products = settingtools.RegionExpressionInventory()
        for payload_part, start_offset in zip(payload_parts, start_offsets):
            timespan = timespantools.Timespan(start_offset)
            product = type(self)([], self.voice_name, timespan.start_offset)
            product._payload = payload_part
            products.append(product)
        return products

    def reflect(self):
        '''Reflect payload about region product axis.

        Operate in place and return region product.
        '''
        payload = self.payload.reflect()
        if payload is not None:
            self._payload = payload
        return self

    def rotate(self, rotation):
        '''Rotate payload by `rotation`.

        Operate in place and return region product.
        '''
        payload = self.payload.rotate(rotation)
        self._payload = payload
        return self

    def translate(self, translation):
        '''Translate region product by `translation`.

        Operate in place and return region product.
        '''
        translation = durationtools.Duration(translation)
        new_start_offset = self.start_offset + translation
        self._start_offset = new_start_offset
        return self
