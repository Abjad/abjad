import abc
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.musicexpressiontools.RegionExpression \
    import RegionExpression


class DivisionRegionExpression(RegionExpression):
    r'''Division region expression.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### PRIVATE METHODS ###

    def evaluate(self):
        r'''Evaluate division region expression.

        Return start-positioned division payload expression.
        '''
        from experimental.tools import musicexpressiontools
        divisions = self.source_expression[:]
        divisions = [musicexpressiontools.Division(x) for x in divisions]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(
            divisions, self.total_duration)
        expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
            payload=divisions,
            start_offset=self.start_offset,
            voice_name=self.voice_name,
            )
        return expression
