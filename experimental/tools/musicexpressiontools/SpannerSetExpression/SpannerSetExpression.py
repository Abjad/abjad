import copy
from abjad.tools import spannertools
from experimental.tools.musicexpressiontools.CounttimeComponentSelectExpressionSetExpression import \
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
        result = self.target_counttime_component_select_expression.evaluate_against_score(score)
        if isinstance(result, list):
            for element in result: 
                leaves = element.payload
                new_spanner = copy.copy(spanner)
                new_spanner(leaves)
        else:
            leaves = result.payload
            new_spanner = copy.copy(spanner)
            new_spanner(leaves)
