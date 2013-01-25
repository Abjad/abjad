import abc
from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools
from experimental.tools.settingtools.TimespanScopedSingleContextSetting import TimespanScopedSingleContextSetting


class TimespanScopedSingleContextRhythmSetting(TimespanScopedSingleContextSetting):
    r'''Rhythm region command.

    Region command indicating durated period of time 
    over which a rhythm-maker will apply.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### SPECIAL METHODS ###

    def __sub__(self, timespan):
        '''Subtract `timespan` from rhythm region command.

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

        Return region command inventory.
        '''
        return TimespanScopedSingleContextSetting.__sub__(self, timespan)
    
    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        '''True when self can fuse `expr` to the end of self. Otherwise false.

        Return boolean.
        '''
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

    # TODO: maybe implement to_rhythm_region_expression() methods on RhythmMakerPayloadExpression, etc.
    def to_rhythm_region_expression(self, score_specification, voice_name, start_offset, division_list):
        from experimental.tools import settingtools
        assert isinstance(start_offset, durationtools.Offset), repr(start_offset)
        assert isinstance(division_list, settingtools.DivisionList), repr(division_list)
        assert isinstance(voice_name, str), repr(voice_name)
        if isinstance(self.expression, settingtools.RhythmMakerPayloadExpression):
            rhythm_maker = self.expression.payload[0]
            assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
            command = settingtools.RhythmMakerRhythmRegionExpression(
                rhythm_maker, voice_name, start_offset, division_list)
        elif isinstance(self.expression, settingtools.StartPositionedRhythmPayloadExpression):
            wrapped_component = componenttools.copy_components_and_covered_spanners([self.expression.payload])[0]
            total_duration = self.timespan.duration
            command_start_offset = self.timespan.start_offset
            command = settingtools.CounttimeComponentRhythmRegionExpression(
                wrapped_component, voice_name, start_offset, total_duration)
        elif isinstance(self.expression, settingtools.RhythmSettingLookupExpression):
            expression = self.expression._evaluate()
            if isinstance(expression, settingtools.RhythmMakerPayloadExpression):
                rhythm_maker = expression.payload[0]
                command = settingtools.RhythmMakerRhythmRegionExpression(
                    rhythm_maker, voice_name, start_offset, division_list)
            elif isinstance(expression, settingtools.StartPositionedRhythmPayloadExpression):
                wrapped_component = componenttools.copy_components_and_covered_spanners([expression.payload])[0]
                total_duration = self.timespan.duration
                command_start_offset = self.timespan.start_offset
                command = settingtools.CounttimeComponentRhythmRegionExpression(
                    wrapped_component, voice_name, start_offset, total_duration)
            else:
                raise TypeError(expression)
        elif isinstance(self.expression, settingtools.CounttimeComponentSelectExpression):
            total_duration = self.timespan.duration
            command_start_offset = self.timespan.start_offset
            command = settingtools.SelectExpressionRhythmRegionExpression(
                self.expression, voice_name, command_start_offset, total_duration)
        else:
            raise TypeError(self.expression)
        return command
