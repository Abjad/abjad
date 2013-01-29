from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.expressiontools.RhythmRegionExpression import RhythmRegionExpression


# TODO: inherit from SelectExpressionRhythmRegionExpression to remove duplicate code?
class LookupExpressionRhythmRegionExpression(RhythmRegionExpression):
    '''Lookup expression rhythm region expression.
    '''

    ### INITIALIZER ###

    # TODO: change to lookup_expression, timespan, voice_name
    def __init__(self, lookup_expression=None, start_offset=None, total_duration=None, voice_name=None):
        self._lookup_expression = lookup_expression
        self._voice_name = voice_name
        self._start_offset = start_offset
        self._total_duration = total_duration

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        expression = self.lookup_expression.evaluate()
        if expression is None:
            return
        assert isinstance(expression, 
            expressiontools.StartPositionedRhythmPayloadExpression), repr(expression)
        expression._start_offset = self.start_offset
        start_offset, stop_offset = self.start_offset, self.start_offset + self.total_duration
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = expression.timespan
        assert not keep_timespan.starts_before_timespan_starts(timespan), repr((timespan, keep_timespan))
        assert timespan.start_offset == keep_timespan.start_offset, repr((timespan, keep_timespan))
        inventory = expression & keep_timespan
        assert len(inventory) == 1
        expression = inventory[0]
        assert isinstance(expression, expressiontools.StartPositionedRhythmPayloadExpression), repr(expression)
        expression.repeat_to_stop_offset(stop_offset)
        return expression

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def lookup_expression(self):
        return self._lookup_expression

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name

    ### PUBLIC METHODS ###

    def prolongs_expr(self, expr):
        if isinstance(expr, type(self)):
            if self.lookup_expression == expr.lookup_expression:
                return True
        return False
