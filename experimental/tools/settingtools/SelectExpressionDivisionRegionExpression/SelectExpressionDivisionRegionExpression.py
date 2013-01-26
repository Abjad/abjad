from abjad.tools import sequencetools
from experimental.tools.settingtools.DivisionRegionExpression import DivisionRegionExpression


class SelectExpressionDivisionRegionExpression(DivisionRegionExpression):
    '''Select expression division region expression.
    '''

    ### INITIALIZER ###

    # TODO: reorder input arguments
    def __init__(self, payload=None, start_offset=None, total_duration=None, voice_name=None):
        from experimental.tools import settingtools
        assert isinstance(payload, settingtools.SelectExpression)
        DivisionRegionExpression.__init__(self, payload=payload,
            start_offset=start_offset, total_duration=total_duration, voice_name=voice_name)

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import settingtools
        expression = self.payload.evaluate()
        if expression is not None:
            divisions = expression.elements
            divisions = [settingtools.Division(x) for x in divisions]
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
            expression = settingtools.StartPositionedDivisionPayloadExpression(
                payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
            return expression
