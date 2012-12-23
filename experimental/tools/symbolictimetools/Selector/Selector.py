import abc
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from experimental.tools.requesttools.Request import Request
from experimental.tools.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class Selector(SymbolicTimespan, Request):
    r'''.. versionadded:: 1.0

    Abstract base class from which concrete selectors inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    def __init__(self, anchor=None, start_identifier=None, stop_identifier=None, 
        time_relation=None, timespan_modifications=None, selector_modifications=None, modifications=None):
        from experimental.tools import symbolictimetools
        assert isinstance(anchor, (symbolictimetools.SymbolicTimespan, str, type(None))), repr(anchor)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        assert time_relation is None or time_relation.is_fully_unloaded, repr(time_relation)
        SymbolicTimespan.__init__(self, timespan_modifications=timespan_modifications)
        Request.__init__(self, modifications=modifications)
        self._anchor = anchor
        self._start_identifier = start_identifier
        self._stop_identifier = stop_identifier
        self._time_relation = time_relation
        selector_modifications = selector_modifications or []
        self._selector_modifications = datastructuretools.ObjectInventory(selector_modifications)

    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        return result

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = Request._keyword_argument_name_value_strings.fget(self)
        if 'selector_modifications=ObjectInventory([])' in result:
            result = list(result)
            result.remove('selector_modifications=ObjectInventory([])')
        if 'timespan_modifications=ObjectInventory([])' in result:
            result = list(result)
            result.remove('timespan_modifications=ObjectInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _apply_selector_modifications(self, elements, start_offset):
        from experimental.tools import settingtools
        evaluation_context = {
            'Duration': durationtools.Duration,
            'NonreducedFraction': mathtools.NonreducedFraction,
            'Offset': durationtools.Offset,
            'Ratio': mathtools.Ratio,
            'RotationIndicator': settingtools.RotationIndicator,
            'self': self,
            'result': None,
            'sequencetools': sequencetools,
            }
        for selector_modification in self._selector_modifications:
            assert 'elements' in selector_modification
            selector_modification = selector_modification.replace('elements', repr(elements))
            selector_modification = selector_modification.replace('start_offset', repr(start_offset))
            elements, start_offset = eval(selector_modification, evaluation_context)
        return elements, start_offset

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty selector modifications list.
        '''
        filtered_result = []
        result = Request._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'selector_modifications=datastructuretools.ObjectInventory([])' in string:
                filtered_result.append(string)
        return filtered_result
    
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
    def start_offset(self):
        from experimental.tools import symbolictimetools
        return symbolictimetools.SymbolicOffset(anchor=self._timespan_abbreviation)

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
    def stop_offset(self):
        from experimental.tools import symbolictimetools
        return symbolictimetools.SymbolicOffset(anchor=self._timespan_abbreviation, edge=Right)

    @property
    def time_relation(self):
        '''Inequality of selector.
        
        Return time_relation or none.
        '''
        return self._time_relation
