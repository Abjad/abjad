import abc
import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import rhythmmakertools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.settingtools.AttributeNameEnumeration import AttributeNameEnumeration


class PayloadCallbackMixin(AbjadObject):
    r'''Payload callback mixin.

    Base class from which payload-carrying expressions inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, payload_callbacks=None):
        from experimental.tools import settingtools
        payload_callbacks = payload_callbacks or []
        self._payload_callbacks = settingtools.CallbackInventory(payload_callbacks)

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        assert isinstance(timespan, timespantools.Timespan), repr(timespan)
        callback = 'result = self.___and__(elements, {!r}, start_offset)'.format(timespan)
        return self._copy_and_append_payload_callback(callback)

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    def __getitem__(self, expr):
        '''Return copy of request with appended callback.
        '''
        callback = 'result = self.___getitem__(elements, start_offset, {!r})'
        callback = callback.format(expr)
        return self._copy_and_append_payload_callback(callback)

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'payload_callbacks=CallbackInventory([])' in result:
            result = list(result)
            result.remove('payload_callbacks=CallbackInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def ___and__(self, elements, timespan, original_start_offset):
        from experimental.tools import settingtools
        if hasattr(elements, '__and__'):
            # translate timespan relative to elements' original start offset
            elements_original_start_offset = elements.start_offset
            timespan = timespan.translate(elements_original_start_offset)
            result = elements & timespan
            assert isinstance(result, timespantools.TimespanInventory), repr(result)
            assert len(result) == 1, repr(result)
            result = result[0]
            translation = result.start_offset - elements_original_start_offset
            result = result.translate(-translation)
            assert result.start_offset == original_start_offset
            return result, result.start_offset
        else:
            if not sequencetools.all_are_numbers(elements):
                elements = [mathtools.NonreducedFraction(x) for x in elements]
            if original_start_offset is None:
                original_start_offset = durationtools.Offset(0)
            division_region_product = settingtools.DivisionRegionProduct(
                payload=elements, voice_name='dummy voice name', start_offset=original_start_offset)
            result = division_region_product & timespan
            result = result[0]
            divisions = result.payload.divisions
            return divisions, result.start_offset

    def ___getitem__(self, elements, original_start_offset, expr):
        assert isinstance(expr, slice)
        if hasattr(elements, '_getitem'):
            result = elements._getitem(expr) 
            return result, result.start_offset
        else:
            start_index, stop_index, stride = expr.indices(len(elements))
            selected_elements = elements[expr]
            elements_before = elements[:start_index]
            if original_start_offset is not None:
                duration_before = sum([self._duration_helper(x) for x in elements_before])
                start_offset = durationtools.Offset(duration_before)
                new_start_offset = original_start_offset + start_offset
            else:
                new_start_offset = None
            return selected_elements, new_start_offset

    def _apply_payload_callbacks(self, elements, start_offset):
        from experimental.tools import settingtools
        evaluation_context = {
            'Duration': durationtools.Duration,
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Offset': durationtools.Offset,
            'Ratio': mathtools.Ratio,
            'RotationIndicator': settingtools.RotationIndicator,
            'Timespan': timespantools.Timespan,
            'elements': elements,
            'self': self,
            'start_offset': start_offset,
            'result': None,
            'sequencetools': sequencetools,
            }
        for callback in self.payload_callbacks:
            assert 'elements' in callback
            evaluation_context['elements'] = elements
            evaluation_context['start_offset'] = start_offset
            exec(callback, evaluation_context)
            elements, start_offset = evaluation_context['result']
        return elements, start_offset

    def _copy_and_append_payload_callback(self, callback):
        result = copy.deepcopy(self)
        result.payload_callbacks.append(callback)
        return result

    def _duration_helper(self, expr):
        if hasattr(expr, 'duration'):
            return expr.duration
        elif hasattr(expr, 'prolated_duration'):
            return expr.prolated_duration
        else:
            duration = durationtools.Duration(expr)
            return duration

    # TODO: eventually insist on _evaluate() method
    #@abc.abstractmethod
    #def _evaluate(self, score_specification=None, voice_name=None):
    #    pass

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty payload_callbacks list.
        '''
        filtered_result = []
        result = AbjadObject._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'payload_callbacks=settingtools.CallbackInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

    def _partition_by_ratio(self, elements, original_start_offset, ratio, part):
        if hasattr(elements, 'partition_by_ratio'):
            parts = elements.partition_by_ratio(ratio)
            selected_part = parts[part]
            return selected_part, selected_part.start_offset
        else:
            parts = sequencetools.partition_sequence_by_ratio_of_lengths(elements, ratio)
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

    def _partition_by_ratio_of_durations(self, elements, original_start_offset, ratio, part):
        if hasattr(elements, 'partition_by_ratio_of_durations'):
            parts = elements.partition_by_ratio_of_durations(ratio)
            selected_part = parts[part]
            return selected_part, selected_part.start_offset
        else:
            def duration_helper(x):
                if hasattr(x, 'prolated_duration'):
                    return x.prolated_duration
                elif hasattr(x, 'duration'):
                    return x.duration
                else:
                    return durationtools.Duration(x)
            element_durations = [duration_helper(x) for x in elements]
            element_tokens = durationtools.durations_to_integers(element_durations)
            token_parts = sequencetools.partition_sequence_by_ratio_of_weights(element_tokens, ratio)
            part_lengths = [len(x) for x in token_parts]
            duration_parts = sequencetools.partition_sequence_by_counts(element_durations, part_lengths)
            element_parts = sequencetools.partition_sequence_by_counts(elements, part_lengths)
            selected_part = element_parts[part]
            duration_parts_before = duration_parts[:part]
            durations_before = [
                sum([durationtools.Duration(x) for x in part_before]) for part_before in duration_parts_before]
            duration_before = sum(durations_before)
            if original_start_offset is None:
                original_start_offset = durationtools.Offset(0)
            new_start_offset = original_start_offset + duration_before
            return selected_part, new_start_offset

    def _reflect(self, elements, original_start_offset):
        if hasattr(elements, 'reflect'):
            elements = elements.reflect() or elements
        elif elements.__class__.__name__ in ('tuple', 'list'):
            elements = type(elements)(reversed(elements))
        else:
            elements = elements.reverse() or elements
        new_start_offset = original_start_offset
        return elements, new_start_offset

    def _repeat_to_duration(self, elements, duration, original_start_offset):
        if hasattr(elements, 'repeat_to_duration'):
            result = elements.repeat_to_duration(duration)
            return result, result.start_offset
        else:
            if not sequencetools.all_are_numbers(elements):
                elements = [mathtools.NonreducedFraction(x) for x in elements]
            elements = sequencetools.repeat_sequence_to_weight_exactly(elements, duration)
            new_start_offset = original_start_offset
            return elements, new_start_offset

    def _repeat_to_length(self, elements, length, original_start_offset):
        if hasattr(elements, 'repeat_to_length'):
            result = elements.repeat_to_length(length)
            return result, result.start_offset
        else:
            elements = sequencetools.repeat_sequence_to_length(elements, length)
            new_start_offset = original_start_offset
            return elements, new_start_offset

    def _rotate(self, elements, n, original_start_offset):
        if hasattr(elements, 'rotate'):
            elements.rotate(n)
        else:
            elements = sequencetools.rotate_sequence(elements, n)
        new_start_offset = original_start_offset
        return elements, new_start_offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload_callbacks(self):
        return self._payload_callbacks

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Return tuple of newly constructed requests with payload_callbacks appended.
        '''
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio(elements, start_offset, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_payload_callback(callback))
        return tuple(result)

    def partition_by_ratio_of_durations(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            callback = \
                'result = self._partition_by_ratio_of_durations(elements, start_offset, {!r}, {!r})'
            callback = callback.format(ratio, part)
            result.append(self._copy_and_append_payload_callback(callback))
        return tuple(result)

    def reflect(self):
        '''Return copy of request with appended callback.
        '''
        callback = 'result = self._reflect(elements, start_offset)'
        return self._copy_and_append_payload_callback(callback)

    def repeat_to_duration(self, duration):
        '''Return copy of request with appended callback.
        '''
        duration = durationtools.Duration(duration)
        callback = 'result = self._repeat_to_duration(elements, {!r}, start_offset)'.format(duration)
        return self._copy_and_append_payload_callback(callback)

    def repeat_to_length(self, length):
        '''Return copy of request with appended callback.
        '''
        assert mathtools.is_nonnegative_integer(length)
        callback = 'result = self._repeat_to_length(elements, {!r}, start_offset)'.format(length)
        return self._copy_and_append_payload_callback(callback)

    def rotate(self, index):
        '''Return copy of request with appended callback.
        '''
        from experimental.tools import settingtools
        assert isinstance(index, (int, durationtools.Duration, settingtools.RotationIndicator))
        callback = 'result = self._rotate(elements, {!r}, start_offset)'.format(index)    
        return self._copy_and_append_payload_callback(callback)
