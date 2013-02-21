import abc
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.specificationtools.RegionExpression import RegionExpression


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
        from experimental.tools import specificationtools
        divisions = self.source_expression[:]
        divisions = [specificationtools.Division(x) for x in divisions]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
        expression = specificationtools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
        return expression
