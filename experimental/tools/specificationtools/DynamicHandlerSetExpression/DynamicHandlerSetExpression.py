from abjad.tools import contexttools
from experimental.tools.specificationtools.CounttimeComponentSelectExpressionSetExpression import \
    CounttimeComponentSelectExpressionSetExpression


class DynamicHandlerSetExpression(CounttimeComponentSelectExpressionSetExpression):
    '''Dynamic handler set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute dynamic handler set expression against `score`.
        '''
        handler = self.source_expression.payload
        leaves = self.target_counttime_component_select_expression.evaluate_against_score(score).payload
        handler(leaves)
