import abc
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools
from experimental.tools.expressiontools.TimespanScopedSingleContextSetExpression import \
    TimespanScopedSingleContextSetExpression


class TimespanScopedSingleContextRhythmSetExpression(TimespanScopedSingleContextSetExpression):
    r'''Timespan-scoped single-context rhythm set expression.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### SPECIAL METHODS ###

    def __sub__(self, timespan):
        '''Subtract `timespan` from set expression.

            >>> source = expressiontools.StartPositionedRhythmPayloadExpression(
            ...     "{ c'16 [ c'8 ] }", start_offset=0)
            >>> timespan = timespantools.Timespan(0, 20)
            >>> timespan_scoped_single_context_rhythm_set_expression = \
            ...     expressiontools.TimespanScopedSingleContextRhythmSetExpression(
            ...     source, timespan, 'Voice 1')

        ::

            >>> result = timespan_scoped_single_context_rhythm_set_expression - timespantools.Timespan(5, 15)

        ::

            >>> z(result)
            expressiontools.TimespanScopedSingleContextSetExpressionInventory([
                expressiontools.TimespanScopedSingleContextRhythmSetExpression(
                    source=expressiontools.StartPositionedRhythmPayloadExpression(
                        payload=containertools.Container(
                            music=({c'16, c'8},)
                            ),
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    target_timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(5, 1)
                        ),
                    target_context_name='Voice 1'
                    ),
                expressiontools.TimespanScopedSingleContextRhythmSetExpression(
                    source=expressiontools.StartPositionedRhythmPayloadExpression(
                        payload=containertools.Container(
                            music=({c'16, c'8},)
                            ),
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    target_timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1)
                        ),
                    target_context_name='Voice 1'
                    )
                ])

        Return timespan-scoped single-context set expression inventory.
        '''
        return TimespanScopedSingleContextSetExpression.__sub__(self, timespan)
    
    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if expr.fresh:
            return False
        if expr.source != self.source:
            return False
        return True

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Return string.
        '''
        return 'rhythm'

    ### PUBLIC METHODS ###

    def evaluate(self, division_list, start_offset, voice_name):
        '''Evaluate timespan-scoped single-context rhythm set expression.

        Return rhythm region expression.
        '''
        from experimental.tools import expressiontools
        assert isinstance(division_list, expressiontools.DivisionList), repr(division_list)
        assert isinstance(start_offset, durationtools.Offset), repr(start_offset)
        assert isinstance(voice_name, str), repr(voice_name)
        if isinstance(self.source, expressiontools.RhythmMakerPayloadExpression):
            rhythm_maker = self.source.payload[0]
            assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
            region_expression = expressiontools.RhythmMakerRhythmRegionExpression(
                rhythm_maker, voice_name, start_offset, division_list)
        elif isinstance(self.source, expressiontools.StartPositionedRhythmPayloadExpression):
            wrapped_component = componenttools.copy_components_and_covered_spanners([self.source.payload])[0]
            total_duration = self.target_timespan.duration
            region_expression_start_offset = self.target_timespan.start_offset
            region_expression = expressiontools.LiteralRhythmRegionExpression(
                wrapped_component, voice_name, start_offset, total_duration)
        elif isinstance(self.source, expressiontools.RhythmSetExpressionLookupExpression):
            expression = self.source.evaluate()
            if isinstance(expression, expressiontools.RhythmMakerPayloadExpression):
                rhythm_maker = expression.payload[0]
                region_expression = expressiontools.RhythmMakerRhythmRegionExpression(
                    rhythm_maker, voice_name, start_offset, division_list)
            elif isinstance(expression, expressiontools.StartPositionedRhythmPayloadExpression):
                wrapped_component = componenttools.copy_components_and_covered_spanners([expression.payload])[0]
                total_duration = self.target_timespan.duration
                region_expression_start_offset = self.target_timespan.start_offset
                region_expression = expressiontools.LiteralRhythmRegionExpression(
                    wrapped_component, voice_name, start_offset, total_duration)
            else:
                raise TypeError(expression)
        elif isinstance(self.source, expressiontools.CounttimeComponentSelectExpression):
            total_duration = self.target_timespan.duration
            region_expression_start_offset = self.target_timespan.start_offset
            region_expression = expressiontools.SelectExpressionRhythmRegionExpression(
                self.source, region_expression_start_offset, total_duration, voice_name)
        else:
            raise TypeError(self.source)
        return region_expression
