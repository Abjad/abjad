# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools.functiontools import attach
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class MarkupSetExpression(LeafSetExpression):
    r'''Markup set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute markup set expression against `score`.
        '''
        markup = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            new_markup = markuptools.Markup(markup)
            attach(new_markup, leaf)
