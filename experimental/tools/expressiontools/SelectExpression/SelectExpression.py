import abc
import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timerelationtools
from experimental.tools.expressiontools.AnchoredExpression import AnchoredExpression
from experimental.tools.expressiontools.PayloadCallbackMixin import PayloadCallbackMixin


class SelectExpression(AnchoredExpression, PayloadCallbackMixin):
    r'''Select expression.

    Abstract base class from which concrete select expressions inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    def __init__(self, anchor=None, voice_name=None, time_relation=None, callbacks=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        assert time_relation is None or time_relation.is_fully_unloaded, repr(time_relation)
        AnchoredExpression.__init__(self, anchor=anchor)
        PayloadCallbackMixin.__init__(self, callbacks=callbacks)
        assert voice_name is not None
        self._voice_name = voice_name
        self._time_relation = time_relation

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def time_relation(self):
        '''Time relation of select expression.
        
        Return time relation or none.
        '''
        return self._time_relation

    @property
    def timespan(self):
        '''SelectExpression timespan.

        Return timespan expression.
        '''
        from experimental.tools import expressiontools
        timespan = expressiontools.TimespanExpression(anchor=self)
        timespan._score_specification = self.score_specification
        return timespan

    @property
    def voice_name(self):
        '''Voice name of select expression.

        Return string.
        '''
        return self._voice_name
