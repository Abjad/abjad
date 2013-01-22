from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import rhythmmakertools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.settingtools.NonstartPositionedPayloadCallbackMixin import NonstartPositionedPayloadCallbackMixin


class StartPositionedPayloadCallbackMixin(NonstartPositionedPayloadCallbackMixin):
    r'''Payload callback mixin.

    Base class from which payload-carrying expressions inherit.
    '''

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        callback = 'result = self.___and__(expression, {!r}, start_offset)'.format(timespan)
        return self._copy_and_append_callback(callback)

    def __getitem__(self, expression):
        '''Return copy of expression with appended callback.
        '''
        callback = 'result = self.___getitem__(expression, start_offset, {!r})'
        callback = callback.format(expression)
        return self._copy_and_append_callback(callback)

    ### PRIVATE METHODS ###

    def ___and__(self, expression, timespan, original_start_offset):
        from experimental.tools import settingtools
        if hasattr(expression, '__and__'):
            # translate timespan relative to expression' original start offset
            expression_original_start_offset = expression.start_offset
            timespan = timespan.translate(expression_original_start_offset)
            result = expression & timespan
            assert isinstance(result, timespantools.TimespanInventory), repr(result)
            assert len(result) == 1, repr(result)
            result = result[0]
            translation = result.start_offset - expression_original_start_offset
            result = result.translate(-translation)
            assert result.start_offset == original_start_offset
            return result, result.start_offset
        else:
            if not sequencetools.all_are_numbers(expression):
                expression = [mathtools.NonreducedFraction(x) for x in expression]
            if original_start_offset is None:
                original_start_offset = durationtools.Offset(0)
            division_product = settingtools.StartPositionedDivisionProduct(
                payload=expression, voice_name='dummy voice name', start_offset=original_start_offset)
            result = division_product & timespan
            result = result[0]
            divisions = result.payload.divisions
            return divisions, result.start_offset

    def ___getitem__(self, expression, original_start_offset, s):
        assert isinstance(s, slice)
        if hasattr(expression, '_getitem'):
            result = expression._getitem(s) 
            return result, result.start_offset
        else:
            start_index, stop_index, stride = s.indices(len(expression))
            selected_expression = expression[s]
            expression_before = expression[:start_index]
            if original_start_offset is not None:
                duration_before = sum([self._duration_helper(x) for x in expression_before])
                start_offset = durationtools.Offset(duration_before)
                new_start_offset = original_start_offset + start_offset
            else:
                new_start_offset = None
            return selected_expression, new_start_offset

    def _apply_callbacks(self, expression, start_offset):
        from experimental.tools import settingtools
        assert isinstance(expression, (settingtools.Expression, settingtools.StartPositionedProduct)), repr(expression)
        evaluation_context = {
            'Duration': durationtools.Duration,
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Offset': durationtools.Offset,
            'Ratio': mathtools.Ratio,
            'RotationIndicator': settingtools.RotationIndicator,
            'Timespan': timespantools.Timespan,
            'expression': expression,
            'self': self,
            'start_offset': start_offset,
            'result': None,
            'sequencetools': sequencetools,
            }
        for callback in self.callbacks:
            assert 'expression' in callback
            evaluation_context['expression'] = expression
            evaluation_context['start_offset'] = start_offset
            exec(callback, evaluation_context)
            expression, start_offset = evaluation_context['result']
        return expression, start_offset

    def _partition_by_ratio(self, expression, original_start_offset, ratio, part):
        if hasattr(expression, 'partition_by_ratio'):
            parts = expression.partition_by_ratio(ratio)
            selected_part = parts[part]
            return selected_part, selected_part.start_offset
        else:
            parts = sequencetools.partition_sequence_by_ratio_of_lengths(expression, ratio)
            selected_part = parts[part]
            parts_before = parts[:part]
            durations_before = [
                sum([durationtools.Duration(x) for x in part_before]) for part_before in parts_before]
            duration_before = sum(durations_before)
            start_offset = durationtools.Offset(duration_before)
            if original_start_offset is None:
                original_start_offset = durationtools.Offset(0)
            new_start_offset = original_start_offset + start_offset
            return selected_part, new_start_offset

    def _partition_by_ratio_of_durations(self, expression, original_start_offset, ratio, part):
        if hasattr(expression, 'partition_by_ratio_of_durations'):
            parts = expression.partition_by_ratio_of_durations(ratio)
            selected_part = parts[part]
            return selected_part, selected_part.start_offset
        else:
            element_durations = [self._duration_helper(x) for x in expression]
            element_tokens = durationtools.durations_to_integers(element_durations)
            token_parts = sequencetools.partition_sequence_by_ratio_of_weights(element_tokens, ratio)
            part_lengths = [len(x) for x in token_parts]
            duration_parts = sequencetools.partition_sequence_by_counts(element_durations, part_lengths)
            element_parts = sequencetools.partition_sequence_by_counts(expression, part_lengths)
            selected_part = element_parts[part]
            duration_parts_before = duration_parts[:part]
            durations_before = [
                sum([durationtools.Duration(x) for x in part_before]) for part_before in duration_parts_before]
            duration_before = sum(durations_before)
            if original_start_offset is None:
                original_start_offset = durationtools.Offset(0)
            new_start_offset = original_start_offset + duration_before
            return selected_part, new_start_offset

    def _reflect(self, expression, original_start_offset):
        if hasattr(expression, 'reflect'):
            expression = expression.reflect() or expression
        elif expression.__class__.__name__ in ('tuple', 'list'):
            expression = type(expression)(reversed(expression))
        else:
            expression = expression.reverse() or expression
        new_start_offset = original_start_offset
        return expression, new_start_offset

    def _repeat_to_duration(self, expression, duration, original_start_offset):
        if hasattr(expression, 'repeat_to_duration'):
            result = expression.repeat_to_duration(duration)
            return result, result.start_offset
        else:
            if not sequencetools.all_are_numbers(expression):
                expression = [mathtools.NonreducedFraction(x) for x in expression]
            expression = sequencetools.repeat_sequence_to_weight_exactly(expression, duration)
            new_start_offset = original_start_offset
            return expression, new_start_offset

    def _repeat_to_length(self, expression, length, original_start_offset):
        if hasattr(expression, 'repeat_to_length'):
            result = expression.repeat_to_length(length)
            return result, result.start_offset
        else:
            expression = sequencetools.repeat_sequence_to_length(expression, length)
            new_start_offset = original_start_offset
            return expression, new_start_offset

    def _rotate(self, expression, n, original_start_offset):
        if hasattr(expression, 'rotate'):
            expression.rotate(n)
        else:
            expression = sequencetools.rotate_sequence(expression, n)
        new_start_offset = original_start_offset
        return expression, new_start_offset

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Return tuple of newly constructed expressions with callbacks appended.
        '''
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio(expression, start_offset, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def partition_by_ratio_of_durations(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio_of_durations(expression, start_offset, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_callback(callback))
        return tuple(result)

    def reflect(self):
        '''Return copy of expression with appended callback.
        '''
        callback = 'result = self._reflect(expression, start_offset)'
        return self._copy_and_append_callback(callback)

    def repeat_to_duration(self, duration):
        '''Return copy of expression with appended callback.
        '''
        duration = durationtools.Duration(duration)
        callback = 'result = self._repeat_to_duration(expression, {!r}, start_offset)'.format(duration)
        return self._copy_and_append_callback(callback)

    def repeat_to_length(self, length):
        '''Return copy of expression with appended callback.
        '''
        assert mathtools.is_nonnegative_integer(length)
        callback = 'result = self._repeat_to_length(expression, {!r}, start_offset)'.format(length)
        return self._copy_and_append_callback(callback)

    def rotate(self, index):
        '''Return copy of expression with appended callback.
        '''
        from experimental.tools import settingtools
        assert isinstance(index, (int, durationtools.Duration, settingtools.RotationIndicator))
        callback = 'result = self._rotate(expression, {!r}, start_offset)'.format(index)    
        return self._copy_and_append_callback(callback)
