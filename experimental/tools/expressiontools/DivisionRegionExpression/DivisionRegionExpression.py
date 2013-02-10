import abc
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.expressiontools.RegionExpression import RegionExpression


class DivisionRegionExpression(RegionExpression):
    '''Division region expression.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate division region expression.

        Return start-positioned division payload expression.
        '''
        from experimental.tools import expressiontools
        divisions = self.source_expression[:]
        divisions = [expressiontools.Division(x) for x in divisions]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
        expression = expressiontools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
        return expression
