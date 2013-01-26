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

    def evaluate(self):
        #raise Exception
        from experimental.tools import settingtools
        expression = self.expression.evaluate()
        if expression is None:
            return
        divisions = expression.elements[:]
        divisions = [settingtools.Division(x) for x in divisions]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.timespan.duration)
        expression = settingtools.StartPositionedDivisionPayloadExpression(
            payload=divisions, start_offset=self.timespan.start_offset, voice_name=self.voice_name)
        return expression

    def to_region_expression(self, voice_name):
        from experimental.tools import settingtools
        start_offset, total_duration = self.timespan.start_offset, self.timespan.duration
        if isinstance(self.expression, settingtools.SelectExpression):
            region_expression = settingtools.SelectExpressionDivisionRegionExpression(
                self.expression, start_offset, total_duration, voice_name)
        elif isinstance(self.expression, settingtools.DivisionSettingLookupExpression):
            expression = self.expression.evaluate()
            if isinstance(expression, settingtools.PayloadExpression):
                divisions = expression.elements
                region_expression = settingtools.SelectExpressionDivisionRegionExpression(
                    divisions, start_offset, total_duration, voice_name)
            else:
                raise TypeError(expression)
        # TODO: maybe combine the following two branches?
        elif isinstance(self.expression, settingtools.PayloadExpression):
            divisions = self.expression.elements
            region_expression = settingtools.LiteralDivisionRegionExpression(
                divisions, start_offset, total_duration, voice_name)
        elif isinstance(self.expression, settingtools.ExpressionInventory):
            divisions = self.expression.elements
            region_expression = settingtools.LiteralDivisionRegionExpression(
                divisions, start_offset, total_duration, voice_name)
        else:
            raise TypeError(self.expression)
        return region_expression
