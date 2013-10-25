# -*- encoding: utf-8 -*-
import copy
import numbers
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import mutationtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from abjad.tools.selectiontools import select
from experimental.tools.musicexpressiontools.IterablePayloadExpression \
    import IterablePayloadExpression


class StartPositionedPayloadExpression(IterablePayloadExpression):
    r'''Start-positioned payload expression.

    Start-positioned payload expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None, voice_name=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        IterablePayloadExpression.__init__(self, payload=payload)
        start_offset = durationtools.Offset(start_offset)
        self._start_offset = start_offset
        self._voice_name = voice_name

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        r'''Keep intersection of start-positioned payload expression 
        and `timespan`.

        Operates in place and returns timespan inventory.
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
            middle_payload_expression = type(self)(
                payload=[],
                start_offset=middle_timespan.start_offset,
                voice_name=self.voice_name,
                )
            middle_payload_expression._payload = middle_payload
            result = timespantools.TimespanInventory(
                [middle_payload_expression])
        else:
            result = timespantools.TimespanInventory()
        return result

    def __getitem__(self, expr):
        r'''Start-positioned payload expression get item.

        Returns newly constructed start-positioned payload expression
        with referenced payload.
        '''
        assert isinstance(expr, (int, slice)), repr(expr)
        if isinstance(expr, slice):
            start, stop, stride = expr.indices(len(self.payload))
            elements_before = self.payload[:start]
            new_payload = self.payload.__getitem__(expr)
        elif isinstance(expr, int):
            elements_before = self.payload[:expr]
            new_payload = [self.payload.__getitem__(expr)]
        else:
            raise ValueError
        duration_before = self._get_duration_of_list(elements_before)
        new_start_offset = self.start_offset + duration_before
        result = self.new(payload=new_payload, start_offset=new_start_offset)
        return result

    def __len__(self):
        r'''Start-positioned payload expression length.

        Returns nonnegative integer.
        '''
        return len(self.payload)

    def __lt__(self, expr):
        r'''True when expression starts before `expr`.

        Also true when expression starts when `expr` starts
        but expression stops before `expr` stops.

        Otherwise false.

        Returns boolean.
        '''
        if self.timespan.starts_before_timespan_starts(expr):
            return True
        elif self.timespan.starts_when_timespan_starts(expr):
            return self.timespan.stops_before_timespan_stops(expr)
        return False

    def __or__(self, expr):
        r'''Logical OR of two payload expressions.

        Payload expression must be able to fuse.

        Returns timespan inventory.
        '''
        assert self._can_fuse(expr)
        if isinstance(self.payload, containertools.Container):
            selection = select(self.payload[0], contiguous=True)
            left = mutationtools.mutate(selection).copy()[0]
            selection = select(expr.payload[0], contiguous=True)
            right = mutationtools.mutate(selection).copy()[0]
            payload = containertools.Container([left, right])
            for component in payload[:]:
                component._extract()
            payload = containertools.Container([payload])
        else:
            payload = self.payload + expr.payload
        result = type(self)(
            [],
            start_offset=self.timespan.start_offset,
            voice_name=self.voice_name,
            )
        result._payload = payload
        return timespantools.TimespanInventory([result])

    def __sub__(self, timespan):
        r'''Subtract `timespan` from start-positioned payload expression.

        Operates in place and returns timespan inventory.
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
            if hasattr(self.payload, 'duration'):
                payload_duration = self.payload.duration
            else:
                payload_duration = self.payload._get_duration()
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
            left_payload_expression = type(self)(
                payload=[],
                start_offset=left_timespan.start_offset,
                voice_name=self.voice_name,
                )
            left_payload_expression._payload = left_payload
            right_timespan = timespantools.Timespan(timespan.stop_offset)
            right_payload_expression = type(self)(
                payload=[],
                start_offset=right_timespan.start_offset,
                voice_name=self.voice_name,
                )
            right_payload_expression._payload = right_payload
            payload_expressions = \
                [left_payload_expression, right_payload_expression]
            result = timespantools.TimespanInventory(payload_expressions)
        else:
            result = timespantools.TimespanInventory([self])
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _duration(self):
        if hasattr(self.payload, 'duration'):
            return self.payload.duration
        else:
            return self._get_duration_of_list(self.payload)

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
        elif hasattr(expr, '_get_duration'):
            return expr._get_duration()
        elif hasattr(expr, 'duration'):
            return expr.duration
        elif isinstance(expr, numbers.Number):
            return durationtools.Duration(expr)
        elif hasattr(expr, '_get_timespan'):
            return expr._get_timespan().duration
        elif hasattr(expr, 'get_timespan'):
            return expr.get_timespan().duration
        elif hasattr(expr, 'timespan'):
            return expr.timespan.duration
        else:
            return durationtools.Duration(expr)

    def _get_duration_of_list(self, expr):
        duration = durationtools.Duration(0)
        for element in expr:
            duration += self._get_duration_of_expr(element)
        return duration

    ### PUBLIC PROPERTIES ###

    @property
    def elements(self):
        r'''Start-positioned payload expression elements.

        Returns tuple or list.
        '''
        return self.payload

    @property
    def elements_are_time_contiguous(self):
        r'''True when start-positioned payload expression elements 
        are time-contiguous.
        Otherwise false.

        Returns boolean.
        '''
        if len(self.elements):
            last_element = self.elements[0]
            for current_element in self.elements[1:]:
                #if not last_element.get_timespan().stop_offset == \
                #    current_element.get_timespan().start_offset:
                if not last_element._get_timespan().stop_offset == \
                    current_element._get_timespan().start_offset:
                    return False
                last_element = current_element
        return True

    @property
    def payload(self):
        r'''Start-postioned payload expression payload.

        Returns tuple or list.
        '''
        return self._payload

    @property
    def start_offset(self):
        r'''Start-positioned payload expression start-offset.

        Returns offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        r'''Start-positioned payload expression stop-offset.

        Returns offset.
        '''
        return self.timespan.stop_offset

    @property
    def timespan(self):
        r'''Start-positioned payload expression timespan.

        Returns timespan.
        '''
        return timespantools.Timespan(self.start_offset, self._stop_offset)

    @property
    def voice_name(self):
        r'''Start-positioned payload expression voice name.

        Returns string.
        '''
        return self._voice_name

    ### PUBLIC METHODS ###

    def get_elements_that_satisfy_time_relation(
        self, 
        time_relation, 
        callback_cache,
        ):
        r'''Get start-positioned payload expression elements that satisfy 
        `time_relation`.

        Returns newly constructed start-positioned payload expression.
        '''
        key = (repr(self), repr(time_relation))
        if key not in callback_cache or not callback_cache[key]:
            start_offsets, stop_offsets = [], []
            for element in self.elements:
                start_offsets.append(element.start_offset)
                stop_offsets.append(element.stop_offset)
            start_index, stop_index = time_relation.get_offset_indices(
                start_offsets, stop_offsets)
            elements = self.elements[start_index:stop_index]
            if not elements:
                return
            callback_cache[key] = elements
        elements = callback_cache[key]
        start_offset = elements[0].start_offset
        expression = self.new(payload=elements, start_offset=start_offset)
        return expression

    def partition_by_ratio(self, ratio):
        r'''Partition start-positioned payload expression by ratio.

        Operates in place and returns newly constructed inventory.
        '''
        from experimental.tools import musicexpressiontools
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(
            self.elements, ratio)
        durations = [self._get_duration_of_list(part) for part in parts]
        payload_parts = self._split_payload_at_offsets(durations)
        start_offsets = mathtools.cumulative_sums(durations)[:-1]
        start_offsets = [
            self.start_offset + start_offset 
            for start_offset in start_offsets]
        payload_expressions = \
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory()
        for payload_part, start_offset in zip(payload_parts, start_offsets):
            timespan = timespantools.Timespan(start_offset)
            payload_expression = type(self)(
                [],
                start_offset=timespan.start_offset,
                voice_name=self.voice_name,
                )
            payload_expression._payload = payload_part
            payload_expressions.append(payload_expression)
        return payload_expressions

    def partition_by_ratio_of_durations(self, ratio):
        r'''Partition start-positioned payload expression 
        by ratio of durations.

        Operates in place and returns newly constructed inventory.
        '''
        from experimental.tools import musicexpressiontools
        element_durations = [
            self._get_duration_of_expr(leaf) for leaf in self.elements]
        integers = self._durations_to_integers(element_durations)
        parts = sequencetools.partition_sequence_by_ratio_of_weights(
            integers, ratio)
        part_lengths = [len(part) for part in parts]
        parts = sequencetools.partition_sequence_by_counts(
            self.elements, part_lengths)
        durations = [self._get_duration_of_list(part) for part in parts]
        payload_parts = self._split_payload_at_offsets(durations)
        start_offsets = mathtools.cumulative_sums(durations)[:-1]
        start_offsets = [
            self.start_offset + start_offset 
            for start_offset in start_offsets]
        payload_expressions = \
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory()
        for payload_part, start_offset in zip(payload_parts, start_offsets):
            timespan = timespantools.Timespan(start_offset)
            payload_expression = type(self)(
                [],
                start_offset=timespan.start_offset,
                voice_name=self.voice_name,
                )
            payload_expression._payload = payload_part
            payload_expressions.append(payload_expression)
        return payload_expressions

    def reflect(self):
        r'''Reflect start-positioned payload expression about axis.

        Operates in place and returns payload expression.
        '''
        payload = self.payload.reflect()
        if payload is not None:
            self._payload = payload
        return self

    def rotate(self, rotation):
        r'''Rotate start-positioned payload expression by `rotation`.

        Operates in place and returns payload expression.
        '''
        payload = self.payload.rotate(rotation)
        self._payload = payload
        return self

    def translate(self, translation):
        r'''Translate start-positioned payload expression by `translation`.

        Operates in place and returns payload expression.
        '''
        translation = durationtools.Duration(translation)
        new_start_offset = self.start_offset + translation
        self._start_offset = new_start_offset
        return self
