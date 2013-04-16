import abc
import copy
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools
from experimental.tools.musicexpressiontools.TimespanScopedSingleContextSetExpression import \
    TimespanScopedSingleContextSetExpression


class TimespanScopedSingleContextRhythmSetExpression(TimespanScopedSingleContextSetExpression):
    r'''Timespan-scoped single-context rhythm set expression.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, source_expression=None, target_timespan=None, target_context_name=None, fresh=None):
        TimespanScopedSingleContextSetExpression.__init__(self, attribute='rhythm',
            source_expression=source_expression, target_timespan=target_timespan,
            target_context_name=target_context_name, fresh=fresh)

    ### SPECIAL METHODS ###

    def __sub__(self, timespan):
        '''Subtract `timespan` from timespan-scoped single-context rhythm set expression.

            >>> source_expression = musicexpressiontools.StartPositionedRhythmPayloadExpression(
            ...     "{ c'16 [ c'8 ] }", start_offset=0)
            >>> timespan = timespantools.Timespan(0, 20)
            >>> timespan_scoped_single_context_rhythm_set_expression = \
            ...     musicexpressiontools.TimespanScopedSingleContextRhythmSetExpression(
            ...     source_expression, timespan, 'Voice 1')

        ::

            >>> result = timespan_scoped_single_context_rhythm_set_expression - timespantools.Timespan(5, 15)

        ::

            >>> z(result)
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory([
                musicexpressiontools.TimespanScopedSingleContextRhythmSetExpression(
                    source_expression=musicexpressiontools.StartPositionedRhythmPayloadExpression(
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
                musicexpressiontools.TimespanScopedSingleContextRhythmSetExpression(
                    source_expression=musicexpressiontools.StartPositionedRhythmPayloadExpression(
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
        if expr.source_expression != self.source_expression:
            return False
        if not self.target_timespan.stops_when_timespan_starts(expr.target_timespan):
            return False
        return True

    ### PUBLIC METHODS ###

    def evaluate(self, division_list, start_offset, voice_name):
        '''Evaluate timespan-scoped single-context rhythm set expression.

        Return rhythm region expression.
        '''
        from experimental.tools import musicexpressiontools
        assert isinstance(division_list, musicexpressiontools.DivisionList), repr(division_list)
        assert isinstance(start_offset, durationtools.Offset), repr(start_offset)
        assert isinstance(voice_name, str), repr(voice_name)
        total_duration = self.target_timespan.duration
        if isinstance(self.source_expression, musicexpressiontools.RhythmMakerExpression):
            rhythm_maker = self.source_expression.payload
            assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
            region_expression = musicexpressiontools.RhythmMakerRhythmRegionExpression(
                rhythm_maker, division_list, start_offset, voice_name)
        elif isinstance(self.source_expression, musicexpressiontools.StartPositionedRhythmPayloadExpression):
            wrapped_component = copy.deepcopy(self.source_expression.payload)
            region_expression = musicexpressiontools.LiteralRhythmRegionExpression(
                wrapped_component, start_offset, total_duration, voice_name)
        # TODO: remove the double indentation of the following branch
        elif isinstance(self.source_expression, musicexpressiontools.RhythmSetExpressionLookupExpression):
            expression = self.source_expression.evaluate()
            if isinstance(expression, musicexpressiontools.RhythmMakerExpression):
                rhythm_maker = expression.payload
                region_expression = musicexpressiontools.RhythmMakerRhythmRegionExpression(
                    rhythm_maker, division_list, start_offset, voice_name)
            elif isinstance(expression, musicexpressiontools.StartPositionedRhythmPayloadExpression):
                wrapped_component = copy.deepcopy(expression.payload)
                region_expression = musicexpressiontools.LiteralRhythmRegionExpression(
                    wrapped_component, start_offset, total_duration, voice_name)
            elif expression is None:
                region_expression = musicexpressiontools.LookupExpressionRhythmRegionExpression(
                    self.source_expression, division_list, self.target_timespan.start_offset,
                    start_offset, total_duration, voice_name)
            else:
                raise TypeError(expression)
        elif isinstance(self.source_expression, musicexpressiontools.CounttimeComponentSelectExpression):
            region_expression = musicexpressiontools.SelectExpressionRhythmRegionExpression(
                self.source_expression, self.target_timespan.start_offset, total_duration, voice_name)
        else:
            raise TypeError(self.source_expression)
        return region_expression
