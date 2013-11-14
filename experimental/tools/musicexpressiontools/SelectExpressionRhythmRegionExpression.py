# -*- encoding: utf-8 -*-
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.musicexpressiontools.RhythmRegionExpression \
    import RhythmRegionExpression


class SelectExpressionRhythmRegionExpression(RhythmRegionExpression):
    r'''Select expression rhythm region expression.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        r'''Evaluate select expression rhythm region expression.

        Returns none when nonevaluable.

        Returns start-positioned rhythm payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        expression = self.source_expression.evaluate()
        if expression is None:
            return
        assert isinstance(expression,
            musicexpressiontools.StartPositionedRhythmPayloadExpression)
        expression._start_offset = self.start_offset
        start_offset, stop_offset = \
            self.start_offset, self.start_offset + self.total_duration
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = expression.timespan
        assert not keep_timespan.starts_before_timespan_starts(timespan)
        assert timespan.start_offset == keep_timespan.start_offset
        inventory = expression & keep_timespan
        assert len(inventory) == 1
        expression = inventory[0]
        assert isinstance(expression,
            musicexpressiontools.StartPositionedRhythmPayloadExpression)
        expression.repeat_to_stop_offset(stop_offset)
        return expression
