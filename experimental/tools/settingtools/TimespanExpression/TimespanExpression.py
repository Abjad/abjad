from experimental.tools.settingtools.AnchoredExpression import AnchoredExpression
from experimental.tools.settingtools.SetMethodMixin import SetMethodMixin
from experimental.tools.settingtools.SelectMethodMixin import SelectMethodMixin
from experimental.tools.settingtools.TimespanCallbackMixin import TimespanCallbackMixin


class TimespanExpression(AnchoredExpression, TimespanCallbackMixin, SelectMethodMixin, SetMethodMixin):
    r'''Timespan expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> setting = red_segment.set_time_signatures([(4, 8), (3, 8)])
        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> setting = blue_segment.set_time_signatures([(9, 16), (3, 16)])

    The examples below refer to the score and segment specifications defined above.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, callbacks=None):
        from experimental.tools import settingtools
        AnchoredExpression.__init__(self, anchor=anchor)
        TimespanCallbackMixin.__init__(self, callbacks=callbacks)

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification='foo'):
        '''Evaluate timespan expression when applied to `score_specification`.

        Return timespan.
        '''
        anchor_timespan = self.score_specification.get_anchor_timespan(self)
        timespan = self._apply_callbacks(anchor_timespan)
        return timespan
