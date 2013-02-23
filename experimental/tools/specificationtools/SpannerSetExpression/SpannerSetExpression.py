import copy
from abjad.tools import spannertools
from experimental.tools.specificationtools.CounttimeComponentSelectExpressionSetExpression import \
    CounttimeComponentSelectExpressionSetExpression


class SpannerSetExpression(CounttimeComponentSelectExpressionSetExpression):
    '''Spanner set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute spanner set expression against `score`.
        '''
        spanner = self.source_expression.payload
        assert isinstance(spanner, spannertools.Spanner), repr(spanner)
        leaves = self.target_counttime_component_select_expression.evaluate_against_score(score).payload
        new_spanner = copy.copy(spanner)
        new_spanner(leaves)
