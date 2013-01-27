from experimental.tools.expressiontools.SingleContextSetExpression import SingleContextSetExpression


class SingleContextRhythmSetExpression(SingleContextSetExpression):
    r'''Single-context set-time signature expression.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, anchor=None, context_name=None, fresh=True, persist=True):
        SingleContextSetExpression.__init__(self, attribute='rhythm', expression=expression, 
            anchor=anchor, context_name=context_name, fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate timespan of single-context set-rhythm expression.

        Return timespan-scoped single-context set-rhythm expression.
        '''
        from experimental.tools import expressiontools
        timespan = self.evaluate_anchor_timespan()
        command = expressiontools.TimespanScopedSingleContextRhythmSetExpression(
            expression=self.expression, timespan=timespan, context_name=self.context_name, fresh=self.fresh)
        return command
