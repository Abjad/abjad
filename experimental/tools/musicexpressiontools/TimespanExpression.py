# -*- encoding: utf-8 -*-
from abjad.tools import timerelationtools
from experimental.tools.musicexpressiontools.AnchoredExpression \
    import AnchoredExpression
from experimental.tools.musicexpressiontools.TimeContiguousSetMethodMixin \
    import TimeContiguousSetMethodMixin
from experimental.tools.musicexpressiontools.SelectMethodMixin \
    import SelectMethodMixin
from experimental.tools.musicexpressiontools.TimespanCallbackMixin \
    import TimespanCallbackMixin


class TimespanExpression(
    AnchoredExpression, 
    TimespanCallbackMixin, 
    SelectMethodMixin,
    TimeContiguousSetMethodMixin):
    r'''Timespan expression.

    Preliminary definitions:

    ::

        >>> score_template = \
        ...     templatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)
        >>> red_segment = score_specification.append_segment(
        ...     name='red')
        >>> set_expression = red_segment.set_time_signatures(
        ...     [(4, 8), (3, 8)])
        >>> blue_segment = score_specification.append_segment(
        ...     name='blue')
        >>> set_expression = blue_segment.set_time_signatures(
        ...     [(9, 16), (3, 16)])

    Timespan expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, callbacks=None):
        from experimental.tools import musicexpressiontools
        AnchoredExpression.__init__(self, anchor=anchor)
        TimespanCallbackMixin.__init__(self, callbacks=callbacks)

    ### PRIVATE METHODS ###

    def evaluate(self):
        r'''Evaluate timespan expression.

        Returns none when nonevaluable.

        Returns timespan when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        result = self._evaluate_anchor_timespan()
        if result is None:
            return
        elif isinstance(result, timerelationtools.Timespan):
            timespan = self._apply_callbacks(result)
            expression = \
                musicexpressiontools.IterablePayloadExpression([timespan])
            return expression
        elif isinstance(result, list):
            timespan_expressions = []
            for timespan in result:
                timespan = self._apply_callbacks(timespan)
                expression = \
                    musicexpressiontools.IterablePayloadExpression([timespan])
                timespan_expressions.append(expression)
            assert len(result) == len(timespan_expressions)
            return timespan_expressions
        else:
            raise TypeError(result)
