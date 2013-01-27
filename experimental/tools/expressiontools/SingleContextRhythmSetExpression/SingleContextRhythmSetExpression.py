from experimental.tools.expressiontools.SingleContextSetExpression import SingleContextSetExpression


class SingleContextRhythmSetExpression(SingleContextSetExpression):
    r'''Single-context time signature set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source=None, target_timespan=None, context_name=None, fresh=True, persist=True):
        SingleContextSetExpression.__init__(self, attribute='rhythm', source=source, 
            target_timespan=target_timespan, context_name=context_name, fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate timespan of single-context rhythm set expression.

        Return timespan-scoped single-context rhythm set expression.
        '''
        from experimental.tools import expressiontools
        timespan = self.evaluate_anchor_timespan()
        command = expressiontools.TimespanScopedSingleContextRhythmSetExpression(
            source=self.source, timespan=timespan, context_name=self.context_name, fresh=self.fresh)
        return command
