from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.specificationtools.CallbackMixin import CallbackMixin


class IterablePayloadCallbackMixin(CallbackMixin):
    '''Payload callback mixin.
    '''

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        '''Logical AND of payload and `timespan`.

        Return copy of expression with callback.
        '''
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        callback = 'result = self._and__(payload_expression, {!r})'.format(timespan)
        return self._copy_and_append_callback(callback)

    def __getitem__(self, payload_expression):
        '''Get payload item.

        Return copy of expression with callback.
        '''
        callback = 'result = self._getitem__(payload_expression, {!r})'
        callback = callback.format(payload_expression)
        return self._copy_and_append_callback(callback)

    ### PRIVATE METHODS ###

    def _and__(self, payload_expression, timespan):
        from experimental.tools import specificationtools
        assert hasattr(payload_expression, '__and__')
        result = payload_expression & timespan
        assert isinstance(result, timespantools.TimespanInventory), repr(result)
        assert len(result) == 1, repr(result)
        result = result[0]
        return result

    def _apply_callbacks(self, payload_expression):
        from experimental.tools import specificationtools
        assert isinstance(payload_expression, specificationtools.PayloadExpression), repr(payload_expression)
        callback_cache = self.score_specification.interpreter.callback_cache
        evaluation_context = {
            'Duration': durationtools.Duration,
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Offset': durationtools.Offset,
            'Ratio': mathtools.Ratio,
            'RotationIndicator': specificationtools.RotationIndicator,
            'Timespan': timespantools.Timespan,
            'callback_cache': callback_cache,
            'payload_expression': payload_expression,
            'self': self,
            'result': None,
            'sequencetools': sequencetools,
            }
        for callback in self.callbacks:
            assert 'payload_expression' in callback
            evaluation_context['payload_expression'] = payload_expression
            exec(callback, evaluation_context)
            payload_expression = evaluation_context['result']
        return payload_expression

    def _getitem__(self, payload_expression, s):
        assert isinstance(s, (slice, int)), repr(s)
        assert hasattr(payload_expression, '__getitem__')
        result = payload_expression.__getitem__(s)
        return result

    def _map_to_each(self, payload_expression):
        result = [element for element in payload_expression]
        return result
        
    def _partition_by_ratio(self, payload_expression, ratio, part, callback_cache):
        assert hasattr(payload_expression, 'partition_by_ratio')
        key = (repr(payload_expression), repr(ratio))
        if key not in callback_cache:
            parts = payload_expression.partition_by_ratio(ratio)
            callback_cache[key] = parts
        parts = callback_cache[key]
        selected_part = parts[part]
        return selected_part

    def _partition_by_ratio_of_durations(self, payload_expression, ratio, part):
        assert hasattr(payload_expression, 'partition_by_ratio_of_durations')
        parts = payload_expression.partition_by_ratio_of_durations(ratio)
        selected_part = parts[part]
        return selected_part

    def _reflect(self, payload_expression):
        assert hasattr(payload_expression, 'reflect'), repr(payload_expression)
        payload_expression = payload_expression.reflect() or payload_expression
        return payload_expression

    def _repeat_to_duration(self, payload_expression, duration):
        assert hasattr(payload_expression, 'repeat_to_duration')
        result = payload_expression.repeat_to_duration(duration)
        return result

    def _repeat_to_length(self, payload_expression, length):
        assert hasattr(payload_expression, 'repeat_to_length')
        result = payload_expression.repeat_to_length(length)
        return result

    def _rotate(self, payload_expression, n):
        payload_expression = payload_expression.rotate(n) or payload_expression
        return payload_expression

    ### PUBLIC METHODS ###

    def map_to_each(self):
        '''Map to each element in payload.

        Return copy of expression with callback.
        '''
        callback = 'result = self._map_to_each(payload_expression)'
        return self._copy_and_append_callback(callback)

    def partition_by_ratio(self, ratio):
        '''Partition payload by `ratio`.

        Return tuple of newly constructed expressions with callbacks.
        '''
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio(payload_expression, {!r}, {!r}, callback_cache)'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition payload by `ratio` of durations.

        Return tuple of newly constructed expressions with callbacks.
        '''
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio_of_durations(payload_expression, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def reflect(self):
        '''Reflect payload.

        Return copy of expression with callback.
        '''
        callback = 'result = self._reflect(payload_expression)'
        return self._copy_and_append_callback(callback)

    def repeat_to_duration(self, duration):
        '''Repeat payload to `duration`.

        Return copy of expression with callback.
        '''
        duration = durationtools.Duration(duration)
        callback = 'result = self._repeat_to_duration(payload_expression, {!r})'.format(duration)
        return self._copy_and_append_callback(callback)

    def repeat_to_length(self, length):
        '''Repeat payload to `length`.

        Return copy of expression with callback.
        '''
        assert mathtools.is_nonnegative_integer(length)
        callback = 'result = self._repeat_to_length(payload_expression, {!r})'.format(length)
        return self._copy_and_append_callback(callback)

    def rotate(self, index):
        '''Rotate payload.

        Return copy of expression with callback.
        '''
        from experimental.tools import specificationtools
        assert isinstance(index, (int, durationtools.Duration, specificationtools.RotationIndicator))
        callback = 'result = self._rotate(payload_expression, {!r})'.format(index)
        return self._copy_and_append_callback(callback)
