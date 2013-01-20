import abc
import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from experimental.tools.settingtools.Expression import Expression
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class Selector(Expression, PayloadCallbackMixin):
    r'''Selector.

    Abstract base class from which concrete selectors inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    def __init__(self, anchor=None, voice_name=None, time_relation=None, callbacks=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        assert time_relation is None or time_relation.is_fully_unloaded, repr(time_relation)
        Expression.__init__(self, anchor=anchor)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        assert voice_name is not None
        self._voice_name = voice_name
        self._time_relation = time_relation

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = PayloadCallbackMixin._keyword_argument_name_value_strings.fget(self)
        if 'callbacks=CallbackInventory([])' in result:
            result = list(result)
            result.remove('callbacks=CallbackInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _evaluate(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty selector callbacks list.
        '''
        filtered_result = []
        result = PayloadCallbackMixin._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'callbacks=settingtools.CallbackInventory([])' in string:
                filtered_result.append(string)
        return filtered_result
    
    ### READ-ONLY PUBLIC PROPERTIES ###

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
