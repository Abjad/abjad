from experimental.tools.expressiontools.SingleContextSetExpression import SingleContextSetExpression


class SingleContextSetDivisionExpression(SingleContextSetExpression):
    r'''Single-context division setting.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, anchor=None, context_name=None, fresh=True, persist=True, truncate=None):
        assert isinstance(truncate, (bool, type(None)))
        SingleContextSetExpression.__init__(self, attribute='divisions', expression=expression, 
            anchor=anchor, context_name=context_name, fresh=fresh, persist=persist)
        self._truncate = truncate

    ### PUBLIC METHODS ###

    def to_timespan_scoped_setting(self):
        '''Evaluate timespan of single-context division setting.

        Return timespan-scoped single-context division setting.
        '''
        from experimental.tools import expressiontools
        anchor_timespan = self.get_anchor_timespan()
        command = expressiontools.TimespanScopedSingleContextSetDivisionExpression(
            expression=self.expression, timespan=anchor_timespan, 
            context_name=self.context_name, fresh=self.fresh, truncate=self.truncate)
        return command
