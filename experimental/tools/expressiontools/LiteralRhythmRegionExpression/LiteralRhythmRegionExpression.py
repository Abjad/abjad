from abjad.tools import componenttools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.expressiontools.RhythmRegionExpression import RhythmRegionExpression


# TODO: maybe inherit from SelectExpressionRhythmRegionExpression?
class LiteralRhythmRegionExpression(RhythmRegionExpression):
    '''Counttime component rhythm region expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, voice_name=None, start_offset=None, total_duration=None):
        self._payload = payload
        self._voice_name = voice_name
        self._start_offset = start_offset
        self._total_duration = total_duration

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        expression = expressiontools.StartPositionedRhythmPayloadExpression(
            [], start_offset=self.start_offset, voice_name=self.voice_name)
        wrapped_component = componenttools.copy_components_and_covered_spanners([self.payload])[0]
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
        assert isinstance(expression, expressiontools.StartPositionedRhythmPayloadExpression), repr(expression)
        expression.repeat_to_stop_offset(stop_offset)
        return expression

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        return self._payload

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name
