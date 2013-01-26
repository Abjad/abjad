import copy
from abjad.tools import sequencetools
from experimental.tools.settingtools.TimespanScopedSingleContextSetting import TimespanScopedSingleContextSetting


class TimespanScopedSingleContextDivisionSetting(TimespanScopedSingleContextSetting):
    r'''Division region expression.

    Region expression indicating durated period of time 
    to which a division-maker will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, timespan=None, context_name=None, fresh=None, truncate=None):
        TimespanScopedSingleContextSetting.__init__(self, 
            expression=expression, timespan=timespan, context_name=context_name, fresh=fresh)
        assert isinstance(truncate, (bool, type(None))), repr(truncate)
        self._truncate = truncate

    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        '''True when self can fuse `expr` to the end of self. Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if self.truncate:
            return False
        if expr.fresh or expr.truncate:
            return False
        if expr.expression != self.expression:
            return False
        return True

    def _evaluate(self):
        from experimental.tools import settingtools
        expression = self.expression._evaluate()
        if expression is None:
            return
        divisions = expression._payload_elements[:]
        divisions = [settingtools.Division(x) for x in divisions]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.timespan.duration)
        expression = settingtools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.timespan.start_offset, voice_name=self.voice_name)
        return expression

    ## READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Return string.
        '''
        return 'divisions'

    @property
    def truncate(self):
        '''Return boolean.
        '''
        return self._truncate

    @property
    def voice_name(self):
        '''Aliased to division region expression `context_name`.

        Return string.
        '''
        return self.context_name

    ### PUBLIC METHODS ###

    def to_region_expression(self, divisions, start_offset, total_duration, voice_name):
        from experimental.tools import settingtools
        expression = settingtools.DivisionRegionExpression(
            payload=divisions, start_offset=start_offset, 
            total_duration=total_duration, voice_name=voice_name)
        return expression
