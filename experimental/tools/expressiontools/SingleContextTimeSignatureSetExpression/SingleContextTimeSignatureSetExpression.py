from experimental.tools.expressiontools.SingleContextSetExpression import SingleContextSetExpression


class SingleContextTimeSignatureSetExpression(SingleContextSetExpression):
    r'''Single-context time signature set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source=None, target_timespan=None, context_name=None, fresh=True, persist=True):
        SingleContextSetExpression.__init__(self, attribute='time_signatures', source=source, 
            target_timespan=target_timespan, context_name=context_name, fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate timespan of single-context time signataure setting.

        Return timespan-scoped single-context time signature set expression.
        '''
        from experimental.tools import expressiontools
        anchor_timespan = self.evaluate_anchor_timespan()
        command = expressiontools.TimeSignatureRegionCommand(
            self.source, self.context_name, anchor_timespan, fresh=self.fresh)
        return command

    def make_time_signatures(self, score_specification):
        from experimental.tools import expressiontools
        if hasattr(self.source, 'evaluate_early'):
            expression = self.source.evaluate_early()
            assert isinstance(expression, expressiontools.PayloadExpression), repr(expression)
            time_signatures = expression.payload
        else:
            expression = self.source.evaluate()
            assert isinstance(expression, expressiontools.PayloadExpression)
            time_signatures = expression.payload[:]
        if time_signatures:
            segment_specification = score_specification.get_start_segment_specification(self.anchor)
            segment_specification._time_signatures = time_signatures[:]
            return time_signatures
