from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.settingtools.FinalizedRhythmRegionExpression import FinalizedRhythmRegionExpression


class SelectExpressionRhythmRegionExpression(FinalizedRhythmRegionExpression):
    '''SelectExpression rhythm region command.
    '''

    ### INITIALIZER ###

    def __init__(self, select_expression=None, voice_name=None, start_offset=None, total_duration=None):
        self._select_expression = select_expression
        self._voice_name = voice_name
        self._start_offset = start_offset
        self._total_duration = total_duration

    ### PRIVATE METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        expression = self.select_expression._evaluate()
        if expression is None:
            return
        assert isinstance(expression, settingtools.StartPositionedRhythmPayloadExpression), repr(expression)
        expression._start_offset = self.start_offset
        start_offset, stop_offset = self.start_offset, self.start_offset + self.total_duration
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = expression.timespan
        assert not keep_timespan.starts_before_timespan_starts(timespan), repr((timespan, keep_timespan))
        assert timespan.start_offset == keep_timespan.start_offset, repr((timespan, keep_timespan))
        inventory = expression & keep_timespan
        assert len(inventory) == 1
        expression = inventory[0]
        assert isinstance(expression, settingtools.StartPositionedRhythmPayloadExpression), repr(expression)
        expression.repeat_to_stop_offset(stop_offset)
        return expression

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def select_expression(self):
        return self._select_expression

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
            if self.select_expression == expr.select_expression:
                return True
        return False
