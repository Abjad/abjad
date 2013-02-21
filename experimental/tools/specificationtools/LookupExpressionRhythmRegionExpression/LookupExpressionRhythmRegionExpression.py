import copy
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.specificationtools.RhythmRegionExpression import RhythmRegionExpression


class LookupExpressionRhythmRegionExpression(RhythmRegionExpression):
    '''Lookup expression rhythm region expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, division_list=None, 
        region_start_offset=None, start_offset=None, total_duration=None, voice_name=None):
        RhythmRegionExpression.__init__(self, source_expression=source_expression, 
            start_offset=start_offset, total_duration=total_duration, voice_name=voice_name)
        self._division_list = division_list
        self._region_start_offset = region_start_offset

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate lookup expression rhythm region expression.
        
        Return none when nonevaluable.

        Return start-positioned rhythm payload expression when evaluable.
        '''
        from experimental.tools import specificationtools
        expression = self.source_expression.evaluate()
        if expression is None:
            return
        if isinstance(expression, specificationtools.RhythmMakerExpression):
            rhythm_maker = expression.payload
            region_expression = specificationtools.RhythmMakerRhythmRegionExpression(
                rhythm_maker, self.division_list, self.start_offset, self.voice_name)
            result = region_expression.evaluate()
        elif isinstance(expression, specificationtools.StartPositionedRhythmPayloadExpression):
            wrapped_component = copy.deepcopy(expression.payload)
            region_expression = specificationtools.LiteralRhythmRegionExpression(
                wrapped_component, self.start_offset, self.total_duration, self.voice_name)
            result = region_expression.evaluate()
        else:
            raise TypeError(expression)
        assert isinstance(result, specificationtools.StartPositionedRhythmPayloadExpression), repr(result)
        return result
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def division_list(self):
        '''Lookup expression rhythm region expression division list.

        Return division list.
        '''
        return self._division_list

    @property
    def region_start_offset(self):
        '''Lookup expression rhythm region expression region start offset.

        Return offset.
        '''
        return self._region_start_offset
