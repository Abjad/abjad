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
        time_relation=None, offset_modifications=None):
        from experimental import symbolictimetools
        assert isinstance(anchor, (symbolictimetools.SymbolicTimespan, str, type(None))), repr(anchor)
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        assert isinstance(time_relation, (timerelationtools.TimespanTimespanTimeRelation, type(None)))
        SymbolicTimespan.__init__(self, offset_modifications=offset_modifications)
        self._anchor = anchor
        self._start_identifier = start_identifier
        self._stop_identifier = stop_identifier
        self._voice_name = voice_name
        self._time_relation = time_relation
        self._flamingo_modifications = []

    ### PRIVATE METHODS ###

    def _evaluate_new_partition_by_ratio(self, elements, original_start_offset, ratio, part):
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(elements, ratio)
        selected_part = parts[part]
        parts_before = parts[:part]
        durations_before = [
            sum([durationtools.Duration(x) for x in part_before]) for part_before in parts_before]
        duration_before = sum(durations_before)
        start_offset = durationtools.Offset(duration_before)
        new_start_offset = original_start_offset + start_offset
        return selected_part, new_start_offset

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
    def start_identifier(self):
        '''Slice selector start identifier.

        Return integer, string, held expression or none.
        '''
        return self._start_identifier

#    @abc.abstractproperty
#    def start_segment_identifier(self):
#        '''Selector start segment identifier.
#
#        Raise exception when no start segment identifier can be found.
#        '''
#        pass

    @property
    def start_segment_identifier(self):
        '''Return anchor when anchor is a string.

        Otherwise delegate to ``self.time_relation.start_segment_identifier``.

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

    ### PUBLIC METHODS ###

    def apply_flamingo_modifications(self, elements, start_offset):
        evaluation_context = {
            'self': self, 
            'Offset': durationtools.Offset, 
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Ratio': mathtools.Ratio,
            }
        for flamingo_modification in self._flamingo_modifications:
            flamingo_modification = flamingo_modification.replace('elements', repr(elements))
            flamingo_modification = flamingo_modification.replace('start_offset', repr(start_offset))
            elements, start_offset = eval(flamingo_modification, evaluation_context)
        return elements, start_offset

    def partition_by_ratio(self, ratio, is_count=True):
        '''Partition self by `ratio`.

        Method mirrors ``sequencetools.partition_sequence_by_ratio_of_lengths()``.
        Method also mirrors ``sequencetools.partition_sequence_by_ratio_of_weights()``.

        Return tuple timespans.
        '''
        from experimental import symbolictimetools
        result = []
        assert not is_count
        for part in range(len(ratio)):
            result.append(symbolictimetools.TimeRatioOperator(self, ratio, part))
        return tuple(result)

    def new_partition_by_ratio(self, ratio):
        result = []
        ratio = mathtools.Ratio(ratio)
        for part in range(len(ratio)):
            selector = copy.deepcopy(self)
            flamingo_modification = 'self._evaluate_new_partition_by_ratio(elements, start_offset, {!r}, {!r})'
            flamingo_modification = flamingo_modification.format(ratio, part)
            selector._flamingo_modifications.append(flamingo_modification)
            result.append(selector)
        return tuple(result)
