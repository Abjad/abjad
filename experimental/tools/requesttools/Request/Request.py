import abc
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import rhythmmakertools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import helpertools


class Request(AbjadObject):
    r'''.. versionadded:: 1.0

    Base class from which other request classes inherit.

    Requests function as setting sources.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, modifications=None):
        modifications = modifications or []
        self._modifications = datastructuretools.ObjectInventory(modifications)

    ### SPECIAL METHODS ###

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
        '''Return copy of request with appended modification.
        '''
#        modification = 'result = elements.__getitem__({!r})'.format(expr)
#        result = copy.deepcopy(self)
#        result.modifications.append(modification)
#        return result
        # TODO: replace the implementation above with the implementation below. I think.
        modification = 'result = self._slice_selected_objects(elements, start_offset, {!r})'
        modification = modification.format(expr)
        result = copy.deepcopy(self)
        result.modifications.append(modification)
        return result

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'modifications=ObjectInventory([])' in result:
            result = list(result)
            result.remove('modifications=ObjectInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _apply_modifications(self, elements, start_offset):
        from experimental.tools import settingtools
        evaluation_context = {
            'Duration': durationtools.Duration,
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Offset': durationtools.Offset,
            'Ratio': mathtools.Ratio,
            'RotationIndicator': settingtools.RotationIndicator,
            'elements': elements,
            'self': self,
            'start_offset': start_offset,
            'result': None,
            'sequencetools': sequencetools,
            }
        for modification in self.modifications:
            assert 'elements' in modification
            evaluation_context['elements'] = copy.deepcopy(elements)
            evaluation_context['start_offset'] = start_offset
            exec(modification, evaluation_context)
            elements, start_offset = evaluation_context['result']
        return elements, start_offset

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty modifications list.
        '''
        filtered_result = []
        result = AbjadObject._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'modifications=datastructuretools.ObjectInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

    def _partition_objects_by_ratio(self, elements, original_start_offset, ratio, part):
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(elements, ratio)
        selected_part = parts[part]
        parts_before = parts[:part]
        durations_before = [
            sum([durationtools.Duration(x) for x in part_before]) for part_before in parts_before]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        new_start_offset = original_start_offset + start_offset
        return selected_part, new_start_offset

    def _partition_objects_by_ratio_of_durations(self, elements, original_start_offset, ratio, part):
        def duration_helper(x):
            if hasattr(x, 'prolated_duration'):
                return x.prolated_duration
            elif hasattr(x, 'duration'):
                return x.duration
            else:
                return durationtools.Duration(x)
        element_durations = [duration_helper(x) for x in elements]
        element_tokens = durationtools.durations_to_nonreduced_fractions_with_common_denominator(
            element_durations)
        common_denominator = element_tokens[0].denominator
        element_tokens = [common_denominator * token for token in element_tokens]
        token_parts = sequencetools.partition_sequence_by_ratio_of_weights(element_tokens, ratio)
        part_lengths = [len(x) for x in token_parts]
        duration_parts = sequencetools.partition_sequence_by_counts(element_durations, part_lengths)
        element_parts = sequencetools.partition_sequence_by_counts(elements, part_lengths)
        selected_part = element_parts[part]
        duration_parts_before = duration_parts[:part]
        durations_before = [
            sum([durationtools.Duration(x) for x in part_before]) for part_before in duration_parts_before]
        duration_before = sum(durations_before)
        new_start_offset = original_start_offset + duration_before
        return selected_part, new_start_offset

    def _repeat_to_length(self, elements, length, original_start_offset):
        elements = sequencetools.repeat_sequence_to_length(elements, length)
        new_start_offset = original_start_offset
        return elements, new_start_offset

    def _reverse(self, elements, original_start_offset):
        if hasattr(elements, 'reverse'):
            result = elements.reverse()
            elements = result or elements
        else:
            raise Exception
        new_start_offset = original_start_offset
        return elements, new_start_offset

    def _rotate(self, elements, n, original_start_offset):
        if hasattr(elements, 'rotate'):
            elements.rotate(n)
        else:
            elements = sequencetools.rotate_sequence(elements, n)
        new_start_offset = original_start_offset
        return elements, new_start_offset

    def _slice_selected_objects(self, elements, original_start_offset, expr):
        assert isinstance(expr, slice)
        start_index, stop_index, stride = expr.indices(len(elements))
        selected_elements = elements[expr]
        elements_before = elements[:start_index]
        duration_before = sum([durationtools.Duration(x) for x in elements_before])
        start_offset = durationtools.Offset(duration_before)
        if original_start_offset is not None:
            new_start_offset = original_start_offset + start_offset
        else:
            new_start_offset = None
        return selected_elements, new_start_offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def modifications(self):
        return self._modifications

    ### PUBLIC METHODS ###

    def partition_objects_by_ratio(self, ratio):
        '''Return tuple of newly constructed requests with modifications appended.
        '''
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            selector = copy.deepcopy(self)
            selector_modification = \
                'result = self._partition_objects_by_ratio(elements, start_offset, {!r}, {!r})'
            selector_modification = selector_modification.format(ratio, part)
            selector.selector_modifications.append(selector_modification)
            result.append(selector)
        return tuple(result)

    def partition_objects_by_ratio_of_durations(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            selector = copy.deepcopy(self)
            selector_modification = \
                'result = self._partition_objects_by_ratio_of_durations(elements, start_offset, {!r}, {!r})'
            selector_modification = selector_modification.format(ratio, part)
            selector.selector_modifications.append(selector_modification)
            result.append(selector)
        return tuple(result)

    def repeat_to_length(self, length):
        '''Return copy of request with appended modification.
        '''
        assert mathtools.is_nonnegative_integer(length)
        modification = 'result = self._repeat_to_length(elements, {!r}, start_offset)'.format(length)
        result = copy.deepcopy(self)
        result.modifications.append(modification)
        return result
        
    def reverse(self):
        '''Return copy of request with appended modification.
        '''
        modification = 'result = self._reverse(elements, start_offset)'
        result = copy.deepcopy(self)
        result.modifications.append(modification)
        return result

    def rotate(self, index):
        '''Return copy of request with appended modification.
        '''
        from experimental.tools import settingtools
        assert isinstance(index, (int, durationtools.Duration, settingtools.RotationIndicator))
        modification = 'result = self._rotate(elements, {!r}, start_offset)'.format(index)    
        result = copy.deepcopy(self)
        result.modifications.append(modification)
        return result
