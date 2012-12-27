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

    def __init__(self, anchor=None, time_relation=None, modifications=None, timespan_modifications=None):
        from experimental.tools import symbolictimetools
        assert isinstance(anchor, (symbolictimetools.SymbolicTimespan, str, type(None))), repr(anchor)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        assert time_relation is None or time_relation.is_fully_unloaded, repr(time_relation)
        Request.__init__(self, modifications=modifications)
        SymbolicTimespan.__init__(self, timespan_modifications=timespan_modifications)
        self._anchor = anchor
        self._time_relation = time_relation

    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        return result

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = Request._keyword_argument_name_value_strings.fget(self)
        if 'timespan_modifications=ObjectInventory([])' in result:
            result = list(result)
            result.remove('timespan_modifications=ObjectInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty selector modifications list.
        '''
        return Request._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
    
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
    def stop_offset(self):
        from experimental.tools import symbolictimetools
        return symbolictimetools.SymbolicOffset(anchor=self._timespan_abbreviation, edge=Right)

    @property
    def time_relation(self):
        '''Time relation of selector.
        
        Return time relation or none.
        '''
        return self._time_relation
