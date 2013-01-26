from abjad.tools import sequencetools
from experimental.tools.settingtools.DivisionRegionExpression import DivisionRegionExpression


class LiteralDivisionRegionExpression(DivisionRegionExpression):
    '''Literal division region expression.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import settingtools
        divisions = [settingtools.Division(x) for x in self.payload]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
        expression = settingtools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
        return expression

