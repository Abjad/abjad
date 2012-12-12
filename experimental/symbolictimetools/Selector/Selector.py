import abc
import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from experimental.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class Selector(SymbolicTimespan):
    r'''.. versionadded:: 1.0

    Abstract base class from which concrete selectors inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    def __init__(self,
        anchor=None, start_identifier=None, stop_identifier=None, voice_name=None, 
        time_relation=None, timespan_modifications=None, selector_modifications=None):
        from experimental import symbolictimetools
        assert isinstance(anchor, (symbolictimetools.SymbolicTimespan, str, type(None))), repr(anchor)
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        assert isinstance(time_relation, (timerelationtools.TimespanTimespanTimeRelation, type(None)))
        assert time_relation is None or time_relation.is_fully_unloaded
        SymbolicTimespan.__init__(self, timespan_modifications=timespan_modifications)
        self._anchor = anchor
        self._start_identifier = start_identifier
        self._stop_identifier = stop_identifier
        self._voice_name = voice_name
        self._time_relation = time_relation
        self._selector_modifications = selector_modifications or []

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = SymbolicTimespan._keyword_argument_name_value_strings.fget(self)
        if 'selector_modifications=[]' in result:
            result = list(result)
            result.remove('selector_modifications=[]')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _apply_selector_modifications(self, elements, start_offset):
        evaluation_context = {
            'self': self, 
            'Offset': durationtools.Offset, 
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Ratio': mathtools.Ratio,
            }
        for selector_modification in self._selector_modifications:
            selector_modification = selector_modification.replace('elements', repr(elements))
            selector_modification = selector_modification.replace('start_offset', repr(start_offset))
            elements, start_offset = eval(selector_modification, evaluation_context)
        return elements, start_offset

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty selector modifications list.
        '''
        filtered_result = []
        result = SymbolicTimespan._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'selector_modifications=[]' in string:
                filtered_result.append(string)
        return filtered_result
    
    def _partition_by_ratio(self, elements, original_start_offset, ratio, part):
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(elements, ratio)
        selected_part = parts[part]
        parts_before = parts[:part]
        durations_before = [
            sum([durationtools.Duration(x) for x in part_before]) for part_before in parts_before]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        new_start_offset = original_start_offset + start_offset
        return selected_part, new_start_offset

    def _partition_by_ratio_of_durations(self, elements, original_start_offset, ratio, part):
        def duration_helper(x):
            if hasattr(x, 'prolated_duration'):
                return x.prolated_duration
            elif hasattr(x, 'duration'):
                return x.duration
            else:
                return durationtools.Duration(x)
        element_durations = [duration_helper(x) for x in elements]
        element_tokens = durationtools.durations_to_nonreduced_fractions_with_common_denominator(element_durations)
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

    def _set_start_segment_identifier(self, segment_identifier):
        assert isinstance(segment_identifier, str)
        if isinstance(self.anchor, str):
            self._anchor = segment_identifier
        else:
            self.anchor._set_start_segment_identifier(segment_identifier)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        return self._anchor

    @property
    def identifiers(self):
        '''Slice selector start- and stop-identifiers.

        Return pair.
        '''
        return self.start_identifier, self.stop_identifier

    @property
    def selector_modifications(self):
        return self._selector_modifications

    @property
    def start_identifier(self):
        '''Slice selector start identifier.

        Return integer, string, held expression or none.
        '''
        return self._start_identifier

    @property
    def start_segment_identifier(self):
        '''Return anchor when anchor is a string.

        Otherwise delegate to ``self.anchor.start_segment_identifier``.

        Return string or none.
        '''
        if isinstance(self.anchor, str):
            return self.anchor
        else:
            return self.anchor.start_segment_identifier

    @property
    def stop_identifier(self):
        '''Slice selector stop identifier.

        Return integer, string, held expression or none.
        '''
        return self._stop_identifier

    @property
    def time_relation(self):
        '''Inequality of selector.
        
        Return time_relation or none.
        '''
        return self._time_relation

    @property
    def voice_name(self):
        '''Slice selector voice name.

        If voice name is set then slice selector is "anchored" to a particular voice.

        If voice name is none then then slice selector is effectively "free floating"
        and is not anchored to a particular voice.

        Some documentation somewhere will eventually have to explain what it means
        for a selector to be "anchored" or "free floating".

        Return string or none.
        '''
        return self._voice_name

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def get_selected_objects(self, score_specification, context_name):
        '''Get selected objects of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return object or list of objects.
        '''
        pass        

    def partition_by_ratio(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            selector = copy.deepcopy(self)
            selector_modification = \
                'self._partition_by_ratio(elements, start_offset, {!r}, {!r})'
            selector_modification = selector_modification.format(ratio, part)
            selector._selector_modifications.append(selector_modification)
            result.append(selector)
        return tuple(result)

    def partition_by_ratio_of_durations(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            selector = copy.deepcopy(self)
            selector_modification = \
                'self._partition_by_ratio_of_durations(elements, start_offset, {!r}, {!r})'
            selector_modification = selector_modification.format(ratio, part)
            selector._selector_modifications.append(selector_modification)
            result.append(selector)
        return tuple(result)
