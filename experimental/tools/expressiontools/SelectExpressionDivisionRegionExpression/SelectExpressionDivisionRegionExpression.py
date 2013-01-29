from abjad.tools import sequencetools
from experimental.tools.expressiontools.DivisionRegionExpression import DivisionRegionExpression


class SelectExpressionDivisionRegionExpression(DivisionRegionExpression):
    '''Select expression division region expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source=None, start_offset=None, total_duration=None, voice_name=None):
        from experimental.tools import expressiontools
        assert isinstance(source, expressiontools.SelectExpression)
        DivisionRegionExpression.__init__(self, source=source,
            start_offset=start_offset, total_duration=total_duration, voice_name=voice_name)

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        expression = self.source.evaluate()
        if expression is not None:
            divisions = expression.elements
            divisions = [expressiontools.Division(x) for x in divisions]
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
            expression = expressiontools.StartPositionedDivisionPayloadExpression(
                payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
            return expression
