# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class DynamicSetExpression(LeafSetExpression):
    r'''Dynamic set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute dynamic set expression against `score`.
        '''
        dynamic_mark = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            for mark in leaf._get_marks(contexttools.DynamicMark):
                mark.detach()
            dynamic = contexttools.DynamicMark(dynamic_mark)
            dynamic.attach(leaf)
