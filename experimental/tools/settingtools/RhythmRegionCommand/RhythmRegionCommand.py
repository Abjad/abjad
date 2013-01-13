import copy
from experimental.tools.settingtools.RegionCommand import RegionCommand


class RhythmRegionCommand(RegionCommand):
    r'''Rhythm region command.

    Region command indicating durated period of time 
    over which a rhythm-maker will apply.
    '''

    ### SPECIAL METHODS ###

    def __sub__(self, timespan):
        '''Subtract `timespan` from rhythm region command.

            >>> expression = settingtools.AbsoluteExpression("{ c'16 [ c'8 ] }")
            >>> timespan = timespantools.Timespan(0, 20)
            >>> rhythm_region_command = settingtools.RhythmRegionCommand(
            ...     expression, 'Voice 1', timespan)

        ::

            >>> result = rhythm_region_command - timespantools.Timespan(5, 15)

        ::

            >>> z(result)
            settingtools.RegionCommandInventory([
                settingtools.RhythmRegionCommand(
                    request=settingtools.AbsoluteExpression(
                        "{ c'16 [ c'8 ] }"
                        ),
                    context_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(5, 1)
                        )
                    ),
                settingtools.RhythmRegionCommand(
                    request=settingtools.AbsoluteExpression(
                        "{ c'16 [ c'8 ] }"
                        ),
                    context_name='Voice 1',
                    timespan=timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1)
                        )
                    )
                ])

        Return region command inventory.
        '''
        return RegionCommand.__sub__(self, timespan)
    
    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        '''True when self can fuse `expr` to the end of self. Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if expr.fresh:
            return False
        if expr.request != self.request:
            return False
        return True

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Return string.
        '''
        return 'rhythm'

    ### PUBLIC METHODS ###

    def prolongs_expr(self, expr):
        from experimental.tools import selectortools
        from experimental.tools import settingtools
        # check that current rhythm command bears a rhythm material request
        current_material_request = self.request
        assert isinstance(current_material_request, selectortools.CounttimeComponentSelector)
        # fuse only if expr is also a rhythm command that bears a rhythm material request
        if not isinstance(expr, settingtools.RhythmRegionCommand):
            return False
        else:
            previous_rhythm_command = expr
        previous_material_request = getattr(previous_rhythm_command, 'request', None)
        if not isinstance(previous_material_request, selectortools.CounttimeComponentSelector):
            return False
        # fuse only if current and previous commands request same material
        if not current_material_request == previous_material_request:
            return False
        return True
