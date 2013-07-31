# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import timerelationtools
from experimental.tools.musicexpressiontools.AnchoredExpression \
    import AnchoredExpression
from experimental.tools.musicexpressiontools.IterablePayloadCallbackMixin \
    import IterablePayloadCallbackMixin
from experimental.tools.musicexpressiontools.SelectMethodMixin \
    import SelectMethodMixin
from experimental.tools.musicexpressiontools.SetMethodMixin \
    import SetMethodMixin


class SelectExpression(
    AnchoredExpression, 
    IterablePayloadCallbackMixin, 
    SelectMethodMixin, 
    SetMethodMixin):
    r'''Select expression.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    def __init__(
        self, anchor=None, 
        voice_name=None, 
        time_relation=None, 
        callbacks=None,
        ):
        assert isinstance(voice_name, (str, type(None)))
        assert isinstance(
            time_relation,
            (timerelationtools.TimeRelation, type(None)))
        assert time_relation is None or time_relation.is_fully_unloaded
        AnchoredExpression.__init__(self, anchor=anchor)
        IterablePayloadCallbackMixin.__init__(self, callbacks=callbacks)
        SelectMethodMixin.__init__(self)
        SetMethodMixin.__init__(self)
        assert voice_name is not None
        self._voice_name = voice_name
        self._time_relation = time_relation

    ### PRIVATE METHODS ###

    def _get_time_relation(self, anchor_timespan):
        if self.time_relation is None:
            time_relation = \
                timerelationtools.timespan_2_starts_during_timespan_1(
                    timespan_1=anchor_timespan)
        else:
            time_relation = self.time_relation.new(timespan_1=anchor_timespan)
        return time_relation

    ### PUBLIC PROPERTIES ###

    @property
    def time_relation(self):
        r'''Select expression time relation.

        Return time relation or none.
        '''
        return self._time_relation

    @property
    def timespan(self):
        r'''Select expression timespan.

        Return timespan expression.
        '''
        from experimental.tools import musicexpressiontools
        timespan = musicexpressiontools.TimespanExpression(anchor=self)
        timespan._score_specification = self.score_specification
        return timespan

    @property
    def voice_name(self):
        r'''Select expression voice name.

        Return string.
        '''
        return self._voice_name
