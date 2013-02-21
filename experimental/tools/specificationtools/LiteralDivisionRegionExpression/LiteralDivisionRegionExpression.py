from abjad.tools import sequencetools
from experimental.tools.specificationtools.DivisionRegionExpression import DivisionRegionExpression


class LiteralDivisionRegionExpression(DivisionRegionExpression):
    '''Literal division region expression.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate literal division region expression.

        Return start-positioned division payload expression.
        '''
        from experimental.tools import specificationtools
        divisions = [specificationtools.Division(x) for x in self.source_expression]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
        expression = specificationtools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
        return expression
