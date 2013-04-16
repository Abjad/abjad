from abjad.tools import sequencetools
from experimental.tools.musicexpressiontools.DivisionRegionExpression import DivisionRegionExpression


class SelectExpressionDivisionRegionExpression(DivisionRegionExpression):
    '''Select expression division region expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, start_offset=None, total_duration=None, voice_name=None):
        from experimental.tools import musicexpressiontools
        assert isinstance(source_expression, musicexpressiontools.SelectExpression)
        DivisionRegionExpression.__init__(self, source_expression=source_expression,
            start_offset=start_offset, total_duration=total_duration, voice_name=voice_name)

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate select expression division region expression.

        Return none when nonevaluable.

        Return start-positioned division payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        expression = self.source_expression.evaluate()
        if expression is not None:
            divisions = expression.elements
            divisions = [musicexpressiontools.Division(x) for x in divisions]
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.total_duration)
            expression = musicexpressiontools.StartPositionedDivisionPayloadExpression(
                payload=divisions, start_offset=self.start_offset, voice_name=self.voice_name)
            return expression
