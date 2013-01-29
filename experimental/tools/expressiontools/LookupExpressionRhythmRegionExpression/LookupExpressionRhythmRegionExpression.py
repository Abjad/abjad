from abjad.tools import componenttools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.expressiontools.RhythmRegionExpression import RhythmRegionExpression


class LookupExpressionRhythmRegionExpression(RhythmRegionExpression):
    '''Lookup expression rhythm region expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source=None, division_list=None, 
        region_start_offset=None, start_offset=None, total_duration=None, voice_name=None):
        self._source = source
        self._division_list = division_list
        self._region_start_offset = region_start_offset
        self._start_offset = start_offset
        self._total_duration = total_duration
        self._voice_name = voice_name

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        expression = self.source.evaluate()
        if expression is None:
            return
        if isinstance(expression, expressiontools.RhythmMakerPayloadExpression):
            rhythm_maker = expression.payload[0]
            region_expression = expressiontools.RhythmMakerRhythmRegionExpression(
                rhythm_maker, self.division_list, self.start_offset, self.voice_name)
            result = region_expression.evaluate()
        elif isinstance(expression, expressiontools.StartPositionedRhythmPayloadExpression):
            wrapped_component = componenttools.copy_components_and_covered_spanners(
                [expression.payload])[0]
            region_expression = expressiontools.LiteralRhythmRegionExpression(
                wrapped_component, self.start_offset, self.total_duration, self.voice_name)
            result = region_expression.evaluate()
        else:
            raise TypeError(expression)
        assert isinstance(result, expressiontools.StartPositionedRhythmPayloadExpression), repr(result)
        return result
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def division_list(self):
        return self._division_list

    @property
    def source(self):
        return self._source

    @property
    def region_start_offset(self):
        return self._region_start_offset

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name
