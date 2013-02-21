from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.specificationtools.RhythmRegionExpression import RhythmRegionExpression


class SelectExpressionRhythmRegionExpression(RhythmRegionExpression):
    '''Select expression rhythm region expression.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate select expression rhythm region expression.
        
        Return none when nonevaluable.

        Return start-positioned rhythm payload expression when evaluable.
        '''
        from experimental.tools import specificationtools
        expression = self.source_expression.evaluate()
        if expression is None:
            return
        assert isinstance(expression, 
            specificationtools.StartPositionedRhythmPayloadExpression), repr(expression)
        expression._start_offset = self.start_offset
        start_offset, stop_offset = self.start_offset, self.start_offset + self.total_duration
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = expression.timespan
        assert not keep_timespan.starts_before_timespan_starts(timespan), repr((timespan, keep_timespan))
        assert timespan.start_offset == keep_timespan.start_offset, repr((timespan, keep_timespan))
        inventory = expression & keep_timespan
        assert len(inventory) == 1
        expression = inventory[0]
        assert isinstance(expression, 
            specificationtools.StartPositionedRhythmPayloadExpression), repr(expression)
        expression.repeat_to_stop_offset(stop_offset)
        return expression
