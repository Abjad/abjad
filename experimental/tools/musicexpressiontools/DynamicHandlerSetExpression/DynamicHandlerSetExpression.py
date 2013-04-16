from abjad.tools import contexttools
from experimental.tools.musicexpressiontools.CounttimeComponentSelectExpressionSetExpression import \
    CounttimeComponentSelectExpressionSetExpression


class DynamicHandlerSetExpression(CounttimeComponentSelectExpressionSetExpression):
    '''Dynamic handler set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute dynamic handler set expression against `score`.
        '''
        handler = self.source_expression.payload
        result = self.target_counttime_component_select_expression.evaluate_against_score(score)
        if isinstance(result, list):
            for element in result:
                leaves = element.payload
                handler(leaves)
        else:
            leaves = result.payload
            handler(leaves)

