from experimental.tools.expressiontools.SingleContextSetExpression import SingleContextSetExpression


class SingleContextSetRhythmExpression(SingleContextSetExpression):
    r'''Single-context set-time signature expression.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, anchor=None, context_name=None, fresh=True, persist=True):
        SingleContextSetExpression.__init__(self, attribute='rhythm', expression=expression, 
            anchor=anchor, context_name=context_name, fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def to_timespan_scoped_set_expression(self):
        '''Evaluate timespan of single-context set-rhythm expression.

        Return timespan-scoped single-context set-rhythm expression.
        '''
        from experimental.tools import expressiontools
        timespan = self.evaluate_anchor_timespan()
        command = expressiontools.TimespanScopedSingleContextSetRhythmExpression(
            expression=self.expression, timespan=timespan, context_name=self.context_name, fresh=self.fresh)
        return command
