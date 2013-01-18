import abc
import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin
from experimental.tools.settingtools.TimespanExpression import TimespanExpression


#class Selector(PayloadCallbackMixin, TimespanExpression):
class Selector(PayloadCallbackMixin):
    r'''Selector.

    Abstract base class from which concrete selectors inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    #def __init__(self, anchor=None, voice_name=None, time_relation=None, 
    #    payload_callbacks=None, timespan_callbacks=None):
    def __init__(self, anchor=None, voice_name=None, time_relation=None, payload_callbacks=None):
        from experimental.tools import settingtools
        #assert isinstance(anchor, (settingtools.TimespanExpression, str, type(None))), repr(anchor)
        assert isinstance(anchor, (settingtools.Expression, str, type(None))), repr(anchor)
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        assert time_relation is None or time_relation.is_fully_unloaded, repr(time_relation)
        PayloadCallbackMixin.__init__(self, payload_callbacks=payload_callbacks)
        #TimespanExpression.__init__(self, timespan_callbacks=timespan_callbacks)
        self._anchor = anchor
        assert voice_name is not None
        self._voice_name = voice_name
        self._time_relation = time_relation

    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        result = type(self)(*self._input_argument_values)
        result._score_specification = self.score_specification
        return result

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = PayloadCallbackMixin._keyword_argument_name_value_strings.fget(self)
        if 'timespan_callbacks=CallbackInventory([])' in result:
            result = list(result)
            result.remove('timespan_callbacks=CallbackInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        payload, timespan = self._get_payload_and_timespan(score_specification)
        return payload

    def _get_timespan(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        payload, timespan = self._get_payload_and_timespan(score_specification)
        #timespan = self._apply_timespan_callbacks(timespan)
        return timespan

    @abc.abstractmethod
    def _get_payload_and_timespan(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty selector payload_callbacks list.
        '''
        filtered_result = []
        result = PayloadCallbackMixin._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'timespan_callbacks=settingtools.CallbackInventory([])' in string:
                filtered_result.append(string)
        return filtered_result
    
#    def _set_start_segment_identifier(self, segment_identifier):
#        assert isinstance(segment_identifier, str)
#        if isinstance(self.anchor, str):
#            self._anchor = segment_identifier
#        else:
#            self.anchor._set_start_segment_identifier(segment_identifier)

    ### READ-ONLY PUBLIC PROPERTIES ###

#    @property
#    def anchor(self):
#        return self._anchor
#
#    @property
#    def start_offset(self):
#        from experimental.tools import settingtools
#        result = settingtools.OffsetExpression(anchor=self._anchor_abbreviation)
#        result._score_specification = self.score_specification
#        return result
#
#    @property
#    def start_segment_identifier(self):
#        '''Return anchor when anchor is a string.
#
#        Otherwise delegate to ``self.anchor.start_segment_identifier``.
#
#        Return string or none.
#        '''
#        if isinstance(self.anchor, str):
#            return self.anchor
#        else:
#            return self.anchor.start_segment_identifier
#
#    @property
#    def stop_offset(self):
#        from experimental.tools import settingtools
#        result = settingtools.OffsetExpression(anchor=self._anchor_abbreviation, edge=Right)
#        result._score_specification = self.score_specification
#        return result

    @property
    def time_relation(self):
        '''Time relation of selector.
        
        Return time relation or none.
        '''
        return self._time_relation

    @property
    def timespan(self):
        '''Selector timespan.

        Return timespan expression.
        '''
        from experimental.tools import settingtools
        timespan = settingtools.TimespanExpression(anchor=self)
        timespan._score_specification = self.score_specification
        return timespan

    @property
    def voice_name(self):
        '''Voice name of selector.

        Return string.
        '''
        return self._voice_name
