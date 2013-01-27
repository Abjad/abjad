import copy
from abjad.tools import sequencetools
from experimental.tools.expressiontools.TimespanScopedSingleContextSetExpression import \
    TimespanScopedSingleContextSetExpression


class TimespanScopedSingleContextDivisionSetExpression(TimespanScopedSingleContextSetExpression):
    r'''Timespan-scoped single-context division set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source=None, timespan=None, context_name=None, fresh=None, truncate=None):
        TimespanScopedSingleContextSetExpression.__init__(self, 
            source=source, timespan=timespan, context_name=context_name, fresh=fresh)
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
        if expr.source != self.source:
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
        '''Aliased to `context_name`.

        Return string.
        '''
        return self.context_name

    ### PUBLIC METHODS ###

    def evaluate(self, voice_name):
        '''Evaluate timespan-scoped single-context division set expression.
        
        Return division region expression.
        '''
        from experimental.tools import expressiontools
        start_offset, total_duration = self.timespan.start_offset, self.timespan.duration
        if isinstance(self.source, expressiontools.SelectExpression):
            region_expression = expressiontools.SelectExpressionDivisionRegionExpression(
                self.source, start_offset, total_duration, voice_name)
        elif isinstance(self.source, expressiontools.DivisionSetExpressionLookupExpression):
            expression = self.source.evaluate()
            assert isinstance(expression, expressiontools.PayloadExpression)
            divisions = expression.elements
            region_expression = expressiontools.LiteralDivisionRegionExpression(
                divisions, start_offset, total_duration, voice_name)
        elif isinstance(self.source, expressiontools.PayloadExpression):
            divisions = self.source.elements
            region_expression = expressiontools.LiteralDivisionRegionExpression(
                divisions, start_offset, total_duration, voice_name)
        else:
            raise TypeError(self.source)
        return region_expression
