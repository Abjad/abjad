# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.tools.musicexpressiontools.DivisionRegionExpression \
    import DivisionRegionExpression


class LiteralDivisionRegionExpression(DivisionRegionExpression):
    r'''Literal division region expression.
    '''

    ### PRIVATE METHODS ###

    def evaluate(self):
        r'''Evaluate literal division region expression.

        Returns start-positioned division payload expression.
        '''
        from experimental.tools import musicexpressiontools
        divisions = []
        for x in self.source_expression:
            if hasattr(x, 'duration'):
                x = x.duration
            division = durationtools.Division(x)
            divisions.append(division)
        divisions = sequencetools.repeat_sequence_to_weight(
            divisions, self.total_duration)
        expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            payload=divisions,
            start_offset=self.start_offset,
            voice_name=self.voice_name,
            )
        return expression