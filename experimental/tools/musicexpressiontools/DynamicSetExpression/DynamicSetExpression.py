from abjad.tools import contexttools
from experimental.tools.musicexpressiontools.LeafSetExpression import LeafSetExpression


class DynamicSetExpression(LeafSetExpression):
    '''Dynamic set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute dynamic set expression against `score`.
        '''
        dynamic_mark = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            contexttools.detach_dynamic_marks_attached_to_component(leaf)
            contexttools.DynamicMark(dynamic_mark)(leaf)
