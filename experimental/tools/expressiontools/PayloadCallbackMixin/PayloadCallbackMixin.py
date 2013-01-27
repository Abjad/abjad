from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.expressiontools.CallbackMixin import CallbackMixin


class PayloadCallbackMixin(CallbackMixin):
    '''Payload callback mixin.
    '''
    
    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        callback = 'result = self.___and__(payload_expression, {!r})'.format(timespan)
        return self._copy_and_append_callback(callback)

    def __getitem__(self, payload_expression):
        '''Return copy of payload_expression with appended callback.
        '''
        callback = 'result = self.___getitem__(payload_expression, {!r})'
        callback = callback.format(payload_expression)
        return self._copy_and_append_callback(callback)

    ### PRIVATE METHODS ###

    def ___and__(self, payload_expression, timespan):
        from experimental.tools import expressiontools
        assert hasattr(payload_expression, '__and__')
        result = payload_expression & timespan
        assert isinstance(result, timespantools.TimespanInventory), repr(result)
        assert len(result) == 1, repr(result)
        result = result[0]
        return result

    def ___getitem__(self, payload_expression, s):
        assert isinstance(s, slice)
        assert hasattr(payload_expression, '__getitem__')
        result = payload_expression.__getitem__(s)
        return result

    def _apply_callbacks(self, payload_expression):
        from experimental.tools import expressiontools
        assert isinstance(payload_expression, expressiontools.PayloadExpression), repr(payload_expression)
        evaluation_context = {
            'Duration': durationtools.Duration,
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Offset': durationtools.Offset,
            'Ratio': mathtools.Ratio,
            'RotationIndicator': expressiontools.RotationIndicator,
            'Timespan': timespantools.Timespan,
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

    def _partition_by_ratio(self, payload_expression, ratio, part):
        assert hasattr(payload_expression, 'partition_by_ratio')
        parts = payload_expression.partition_by_ratio(ratio)
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

    def partition_by_ratio(self, ratio):
        '''Return tuple of newly constructed payload_expressions with callbacks appended.
        '''
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio(payload_expression, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def partition_by_ratio_of_durations(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio_of_durations(payload_expression, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def reflect(self):
        '''Return copy of payload_expression with appended callback.
        '''
        callback = 'result = self._reflect(payload_expression)'
        return self._copy_and_append_callback(callback)

    def repeat_to_duration(self, duration):
        '''Return copy of payload_expression with appended callback.
        '''
        duration = durationtools.Duration(duration)
        callback = 'result = self._repeat_to_duration(payload_expression, {!r})'.format(duration)
        return self._copy_and_append_callback(callback)

    def repeat_to_length(self, length):
        '''Return copy of payload_expression with appended callback.
        '''
        assert mathtools.is_nonnegative_integer(length)
        callback = 'result = self._repeat_to_length(payload_expression, {!r})'.format(length)
        return self._copy_and_append_callback(callback)

    def rotate(self, index):
        '''Return copy of payload_expression with appended callback.
        '''
        from experimental.tools import expressiontools
        assert isinstance(index, (int, durationtools.Duration, expressiontools.RotationIndicator))
        callback = 'result = self._rotate(payload_expression, {!r})'.format(index)    
        return self._copy_and_append_callback(callback)
