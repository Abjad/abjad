from abjad.tools import contexttools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class DynamicHandlerSetExpression(LeafSetExpression):
    '''Dynamic handler set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute dynamic handler set expression against `score`.
        '''
        handler = self.source_expression.payload
        leaves = self._iterate_leaves_in_score(score)
        handler(leaves)
