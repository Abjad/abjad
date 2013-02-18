import copy
from abjad.tools import sequencetools
from experimental.tools.expressiontools.TimespanScopedSingleContextSetExpression import \
    TimespanScopedSingleContextSetExpression


class TimespanScopedSingleContextDivisionSetExpression(TimespanScopedSingleContextSetExpression):
    r'''Timespan-scoped single-context division set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, target_timespan=None, target_context_name=None, 
        fresh=None, truncate=None):
        TimespanScopedSingleContextSetExpression.__init__(self, attribute='divisions',
            source_expression=source_expression, target_timespan=target_timespan, 
            target_context_name=target_context_name, fresh=fresh)
        assert isinstance(truncate, (bool, type(None))), repr(truncate)
        self._truncate = truncate

    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if self.truncate:
            return False
        if expr.fresh or expr.truncate:
            return False
        if expr.source_expression != self.source_expression:
            return False
        if not self.target_timespan.stops_when_timespan_starts(expr.target_timespan):
            return False
        return True

    ## READ-ONLY PUBLIC PROPERTIES ###

    @property
    def truncate(self):
        '''True when timespan-scoped single-context division set expression
        should truncate at segment boundaries.
        Otherwise false.

        Return boolean.
        '''
        return self._truncate

    @property
    def voice_name(self):
        '''Aliased to `target_context_name`.

        Return string.
        '''
        return self.target_context_name

    ### PUBLIC METHODS ###

    def evaluate(self, voice_name):
        '''Evaluate timespan-scoped single-context division set expression.
        
        Return division region expression.
        '''
        from experimental.tools import expressiontools
        start_offset, total_duration = self.target_timespan.start_offset, self.target_timespan.duration
        if isinstance(self.source_expression, expressiontools.SelectExpression):
            region_expression = expressiontools.SelectExpressionDivisionRegionExpression(
                self.source_expression, start_offset, total_duration, voice_name)
        elif isinstance(self.source_expression, expressiontools.DivisionSetExpressionLookupExpression):
            expression = self.source_expression.evaluate()
            assert isinstance(expression, expressiontools.IterablePayloadExpression)
            divisions = expression.elements
            region_expression = expressiontools.LiteralDivisionRegionExpression(
                divisions, start_offset, total_duration, voice_name)
        elif isinstance(self.source_expression, expressiontools.IterablePayloadExpression):
            divisions = self.source_expression.elements
            region_expression = expressiontools.LiteralDivisionRegionExpression(
                divisions, start_offset, total_duration, voice_name)
        else:
            raise TypeError(self.source_expression)
        return region_expression
