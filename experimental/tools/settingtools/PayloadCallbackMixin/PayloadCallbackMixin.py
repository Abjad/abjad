from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.settingtools.CallbackMixin import CallbackMixin


class PayloadCallbackMixin(CallbackMixin):
    '''Nonstart-positioned payload callback mixin.
    '''
    
    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        callback = 'result = self.___and__(expression, {!r})'.format(timespan)
        return self._copy_and_append_callback(callback)

    def __eq__(self, expression):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expression, type(self)):
            return False
        if not self._positional_argument_values == expression._positional_argument_values:
            return False
        return self._keyword_argument_values == expression._keyword_argument_values

    def __getitem__(self, expression):
        '''Return copy of expression with appended callback.
        '''
        callback = 'result = self.___getitem__(expression, {!r})'
        callback = callback.format(expression)
        return self._copy_and_append_callback(callback)

    ### PRIVATE METHODS ###

    def ___and__(self, expression, timespan):
        from experimental.tools import settingtools
        assert hasattr(expression, '__and__')
        result = expression & timespan
        assert isinstance(result, timespantools.TimespanInventory), repr(result)
        assert len(result) == 1, repr(result)
        result = result[0]
        return result

    def ___getitem__(self, expression, s):
        assert isinstance(s, slice)
        if hasattr(expression, '_getitem'):
            result = expression._getitem(s) 
            return result
        else:
            start_index, stop_index, stride = s.indices(len(expression))
            selected_expression = expression[s]
            return selected_expression

    def _apply_callbacks(self, expression):
        from experimental.tools import settingtools
        #assert isinstance(expression, settingtools.Expression), repr(expression)
        evaluation_context = {
            'Duration': durationtools.Duration,
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Offset': durationtools.Offset,
            'Ratio': mathtools.Ratio,
            'RotationIndicator': settingtools.RotationIndicator,
            'Timespan': timespantools.Timespan,
            'expression': expression,
            'self': self,
            'result': None,
            'sequencetools': sequencetools,
            }
        for callback in self.callbacks:
            assert 'expression' in callback
            evaluation_context['expression'] = expression
            exec(callback, evaluation_context)
            expression = evaluation_context['result']
        return expression

    def _duration_helper(self, expression):
        if hasattr(expression, 'duration'):
            return expression.duration
        elif hasattr(expression, 'prolated_duration'):
            return expression.prolated_duration
        else:
            duration = durationtools.Duration(expression)
            return duration

    def _partition_by_ratio(self, expression, ratio, part):
        if hasattr(expression, 'partition_by_ratio'):
            parts = expression.partition_by_ratio(ratio)
            selected_part = parts[part]
            return selected_part
        else:
            parts = sequencetools.partition_sequence_by_ratio_of_lengths(expression, ratio)
            selected_part = parts[part]
            return selected_part

    def _partition_by_ratio_of_durations(self, expression, ratio, part):
        if hasattr(expression, 'partition_by_ratio_of_durations'):
            parts = expression.partition_by_ratio_of_durations(ratio)
            selected_part = parts[part]
            return selected_part
        else:
            element_durations = [self._duration_helper(x) for x in expression]
            element_tokens = durationtools.durations_to_integers(element_durations)
            token_parts = sequencetools.partition_sequence_by_ratio_of_weights(element_tokens, ratio)
            part_lengths = [len(x) for x in token_parts]
            duration_parts = sequencetools.partition_sequence_by_counts(element_durations, part_lengths)
            element_parts = sequencetools.partition_sequence_by_counts(expression, part_lengths)
            selected_part = element_parts[part]
            return selected_part

    def _reflect(self, expression):
        if hasattr(expression, 'reflect'):
            expression = expression.reflect() or expression
        elif expression.__class__.__name__ in ('tuple', 'list'):
            expression = type(expression)(reversed(expression))
        else:
            expression = expression.reverse() or expression
        return expression

    def _repeat_to_duration(self, expression, duration):
        assert hasattr(expression, 'repeat_to_duration')
        result = expression.repeat_to_duration(duration)
        return result

    def _repeat_to_length(self, expression, length):
        assert hasattr(expression, 'repeat_to_length')
        result = expression.repeat_to_length(length)
        return result

    def _rotate(self, expression, n):
        expression = expression.rotate(n) or expression
        return expression

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Return tuple of newly constructed expressions with callbacks appended.
        '''
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio(expression, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def partition_by_ratio_of_durations(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio_of_durations(expression, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def reflect(self):
        '''Return copy of expression with appended callback.
        '''
        callback = 'result = self._reflect(expression)'
        return self._copy_and_append_callback(callback)

    def repeat_to_duration(self, duration):
        '''Return copy of expression with appended callback.
        '''
        duration = durationtools.Duration(duration)
        callback = 'result = self._repeat_to_duration(expression, {!r})'.format(duration)
        return self._copy_and_append_callback(callback)

    def repeat_to_length(self, length):
        '''Return copy of expression with appended callback.
        '''
        assert mathtools.is_nonnegative_integer(length)
        callback = 'result = self._repeat_to_length(expression, {!r})'.format(length)
        return self._copy_and_append_callback(callback)

    def rotate(self, index):
        '''Return copy of expression with appended callback.
        '''
        from experimental.tools import settingtools
        assert isinstance(index, (int, durationtools.Duration, settingtools.RotationIndicator))
        callback = 'result = self._rotate(expression, {!r})'.format(index)    
        return self._copy_and_append_callback(callback)
