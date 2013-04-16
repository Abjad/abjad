from abjad.tools import mathtools
from experimental.tools.musicexpressiontools.SingleContextSetExpression import SingleContextSetExpression


class SingleContextTimeSignatureSetExpression(SingleContextSetExpression):
    r'''Single-context time signature set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, target_timespan=None, target_context_name=None, fresh=True, persist=True):
        SingleContextSetExpression.__init__(self, attribute='time_signatures', source_expression=source_expression,
            target_timespan=target_timespan, target_context_name=target_context_name,
            fresh=fresh, persist=persist)

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate single-context time signature set expression.

        Return timespan-scoped single-context time signature set expression.
        '''
        from experimental.tools import musicexpressiontools
        target_timespan = self._evaluate_anchor_timespan()
        expression = musicexpressiontools.TimespanScopedSingleContextTimeSignatureExpression(
            source_expression=self.source_expression, target_timespan=target_timespan,
            target_context_name=self.target_context_name, fresh=self.fresh)
        expression._lexical_rank = self._lexical_rank
        return expression

    def make_time_signatures(self):
        from experimental.tools import musicexpressiontools
        if hasattr(self.source_expression, 'evaluate_early'):
            expression = self.source_expression.evaluate_early()
            assert isinstance(expression, musicexpressiontools.IterablePayloadExpression), repr(expression)
            time_signatures = expression.payload
        else:
            expression = self.source_expression.evaluate()
            assert isinstance(expression, musicexpressiontools.IterablePayloadExpression)
            time_signatures = expression.payload[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        if time_signatures:
            self.root_specification._time_signatures = time_signatures[:]
            return time_signatures
