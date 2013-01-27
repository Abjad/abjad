import copy
from abjad.tools import sequencetools
from experimental.tools.expressiontools.TimespanScopedSingleContextSetExpression import TimespanScopedSingleContextSetExpression


class TimespanScopedSingleContextSetDivisionExpression(TimespanScopedSingleContextSetExpression):
    r'''Division region expression.

    Region expression indicating durated period of time 
    to which a division-maker will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, timespan=None, context_name=None, fresh=None, truncate=None):
        TimespanScopedSingleContextSetExpression.__init__(self, 
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

    def evaluate(self, voice_name):
        '''Evaluate timespan-scoped single-context set-division expression.
        
        Return division region expression.
        '''
        from experimental.tools import expressiontools
        start_offset, total_duration = self.timespan.start_offset, self.timespan.duration
        if isinstance(self.expression, expressiontools.SelectExpression):
            region_expression = expressiontools.SelectExpressionDivisionRegionExpression(
                self.expression, start_offset, total_duration, voice_name)
        elif isinstance(self.expression, expressiontools.SetDivisionLookupExpression):
            expression = self.expression.evaluate()
            assert isinstance(expression, expressiontools.PayloadExpression)
            divisions = expression.elements
            region_expression = expressiontools.LiteralDivisionRegionExpression(
                divisions, start_offset, total_duration, voice_name)
        elif isinstance(self.expression, expressiontools.PayloadExpression):
            divisions = self.expression.elements
            region_expression = expressiontools.LiteralDivisionRegionExpression(
                divisions, start_offset, total_duration, voice_name)
        else:
            raise TypeError(self.expression)
        return region_expression
