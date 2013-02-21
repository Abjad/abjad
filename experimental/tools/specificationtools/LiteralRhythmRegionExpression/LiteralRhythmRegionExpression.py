import copy
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.specificationtools.RhythmRegionExpression import RhythmRegionExpression


class LiteralRhythmRegionExpression(RhythmRegionExpression):
    '''Literal rhythm region expression.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import specificationtools
        expression = specificationtools.StartPositionedRhythmPayloadExpression(
            [], start_offset=self.start_offset, voice_name=self.voice_name)
        wrapped_component = copy.deepcopy(self.source_expression)
        expression._payload = wrapped_component
        start_offset, stop_offset = self.start_offset, self.start_offset + self.total_duration
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = expression.timespan
        assert not keep_timespan.starts_before_timespan_starts(timespan), repr((timespan, keep_timespan))
        assert timespan.start_offset == keep_timespan.start_offset, repr((timespan, keep_timespan))
        expression = expression & keep_timespan
        assert isinstance(expression, timespantools.TimespanInventory), repr(expression)
        assert len(expression) == 1
        expression = expression[0]
        assert isinstance(expression, specificationtools.StartPositionedRhythmPayloadExpression), repr(expression)
        expression.repeat_to_stop_offset(stop_offset)
        return expression
