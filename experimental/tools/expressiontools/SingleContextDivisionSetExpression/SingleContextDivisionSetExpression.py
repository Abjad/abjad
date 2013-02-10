from experimental.tools.expressiontools.SingleContextSetExpression import SingleContextSetExpression


class SingleContextDivisionSetExpression(SingleContextSetExpression):
    r'''Single-context division set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, target_timespan=None, target_context_name=None, 
        fresh=True, persist=True, truncate=None):
        assert isinstance(truncate, (bool, type(None)))
        SingleContextSetExpression.__init__(self, attribute='divisions', source_expression=source_expression, 
            target_timespan=target_timespan, target_context_name=target_context_name, 
            fresh=fresh, persist=persist)
        self._truncate = truncate

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate single-context division set expression.

        Return timespan-scoped single-context division set expression.
        '''
        from experimental.tools import expressiontools
        target_timespan = self._evaluate_anchor_timespan()
        expression = expressiontools.TimespanScopedSingleContextDivisionSetExpression(
            source_expression=self.source_expression, target_timespan=target_timespan, 
            target_context_name=self.target_context_name, 
            fresh=self.fresh, truncate=self.truncate)
        expression._lexical_rank = self._lexical_rank
        return expression
