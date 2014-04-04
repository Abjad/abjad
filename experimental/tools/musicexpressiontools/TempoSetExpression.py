# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class TempoSetExpression(LeafSetExpression):
    r'''Tempo set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute tempo set expression against `score`.
        '''
        tempo = self.source_expression.payload
        first_leaf = self._iterate_selected_leaves_in_score(score)[0]
        attach(tempo, first_leaf)