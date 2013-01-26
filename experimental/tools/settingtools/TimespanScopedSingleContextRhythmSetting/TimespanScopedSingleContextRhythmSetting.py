import abc
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools
from experimental.tools.settingtools.TimespanScopedSingleContextSetting import TimespanScopedSingleContextSetting


class TimespanScopedSingleContextRhythmSetting(TimespanScopedSingleContextSetting):
    r'''Timespan-scoped single-context rhythm setting.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### SPECIAL METHODS ###

    def __sub__(self, timespan):
        '''Subtract `timespan` from setting.

            >>> expression = settingtools.StartPositionedRhythmPayloadExpression(
            ...     "{ c'16 [ c'8 ] }", start_offset=0)
            >>> timespan = timespantools.Timespan(0, 20)
            >>> timespan_scoped_single_context_rhythm_setting = settingtools.TimespanScopedSingleContextRhythmSetting(
            ...     expression, timespan, 'Voice 1')

        ::

            >>> result = timespan_scoped_single_context_rhythm_setting - timespantools.Timespan(5, 15)

        ::

            >>> z(result)
            settingtools.TimespanScopedSingleContextSettingInventory([
                settingtools.TimespanScopedSingleContextRhythmSetting(
                    expression=settingtools.StartPositionedRhythmPayloadExpression(
                        payload=containertools.Container(
                            music=({c'16, c'8},)
                            ),
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(5, 1)
                        ),
                    context_name='Voice 1'
                    ),
                settingtools.TimespanScopedSingleContextRhythmSetting(
                    expression=settingtools.StartPositionedRhythmPayloadExpression(
                        payload=containertools.Container(
                            music=({c'16, c'8},)
                            ),
                        start_offset=durationtools.Offset(0, 1)
                        ),
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1)
                        ),
                    context_name='Voice 1'
                    )
                ])

        Return timespan-scoped single-context setting inventory.
        '''
        return TimespanScopedSingleContextSetting.__sub__(self, timespan)
    
    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if expr.fresh:
            return False
        if expr.expression != self.expression:
            return False
        return True

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Return string.
        '''
        return 'rhythm'

    ### PUBLIC METHODS ###

    def to_region_expression(self, division_list, start_offset, voice_name):
        from experimental.tools import settingtools
        assert isinstance(division_list, settingtools.DivisionList), repr(division_list)
        assert isinstance(start_offset, durationtools.Offset), repr(start_offset)
        assert isinstance(voice_name, str), repr(voice_name)
        if isinstance(self.expression, settingtools.RhythmMakerPayloadExpression):
            rhythm_maker = self.expression.payload[0]
            assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
            region_expression = settingtools.RhythmMakerRhythmRegionExpression(
                rhythm_maker, voice_name, start_offset, division_list)
        elif isinstance(self.expression, settingtools.StartPositionedRhythmPayloadExpression):
            wrapped_component = componenttools.copy_components_and_covered_spanners([self.expression.payload])[0]
            total_duration = self.timespan.duration
            region_expression_start_offset = self.timespan.start_offset
            region_expression = settingtools.LiteralRhythmRegionExpression(
                wrapped_component, voice_name, start_offset, total_duration)
        elif isinstance(self.expression, settingtools.RhythmSettingLookupExpression):
            expression = self.expression._evaluate()
            if isinstance(expression, settingtools.RhythmMakerPayloadExpression):
                rhythm_maker = expression.payload[0]
                region_expression = settingtools.RhythmMakerRhythmRegionExpression(
                    rhythm_maker, voice_name, start_offset, division_list)
            elif isinstance(expression, settingtools.StartPositionedRhythmPayloadExpression):
                wrapped_component = componenttools.copy_components_and_covered_spanners([expression.payload])[0]
                total_duration = self.timespan.duration
                region_expression_start_offset = self.timespan.start_offset
                region_expression = settingtools.LiteralRhythmRegionExpression(
                    wrapped_component, voice_name, start_offset, total_duration)
            else:
                raise TypeError(expression)
        elif isinstance(self.expression, settingtools.CounttimeComponentSelectExpression):
            total_duration = self.timespan.duration
            region_expression_start_offset = self.timespan.start_offset
            region_expression = settingtools.SelectExpressionRhythmRegionExpression(
                self.expression, voice_name, region_expression_start_offset, total_duration)
        else:
            raise TypeError(self.expression)
        return region_expression
