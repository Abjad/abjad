from abjad.tools import sequencetools
from experimental.tools.expressiontools.DivisionRegionExpression import DivisionRegionExpression


class LiteralDivisionRegionExpression(DivisionRegionExpression):
    '''Literal division region expression.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        divisions = [expressiontools.Division(x) for x in self.source_expression]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
        expression = expressiontools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
        return expression

