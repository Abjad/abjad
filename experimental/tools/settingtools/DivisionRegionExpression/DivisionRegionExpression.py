from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.settingtools.RegionExpression import RegionExpression


class DivisionRegionExpression(RegionExpression):
    '''Division region expression.

    Expression to evaluate to a start-positioned division payload expression.
    '''

    ### PRIVATE METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        divisions = self.payload[:]
        divisions = [settingtools.Division(x) for x in divisions]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
        expression = settingtools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
        return expression
