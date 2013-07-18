from abjad.tools import contexttools
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class DynamicSetExpression(LeafSetExpression):
    '''Dynamic set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute dynamic set expression against `score`.
        '''
        dynamic_mark = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            leaf.select().detach_marks(contexttools.DynamicMark)
            contexttools.DynamicMark(dynamic_mark)(leaf)
