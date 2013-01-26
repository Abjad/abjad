from experimental.tools.settingtools.DivisionRegionExpression import DivisionRegionExpression


class LiteralDivisionRegionExpression(DivisionRegionExpression):
    '''Literal division region expression.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import settingtools
        #divisions = self.payload[:]
        #divisions = [settingtools.Division(x) for x in divisions]
        #divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
        divisions = sequencetools.repeat_sequence_to_weight_exactly(self.payload, self.total_duration)
        expression = settingtools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
        return expression

