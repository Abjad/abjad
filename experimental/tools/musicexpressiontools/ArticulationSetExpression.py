# -*- encoding: utf-8 -*-
import copy
from abjad.tools import marktools
from abjad.tools.scoretools import attach
from abjad.tools.selectiontools import select
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class ArticulationSetExpression(LeafSetExpression):
    r'''Articulation set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute articulation set expression against `score`.
        '''
        articulation_list = self.source_expression.payload
        leaves = self._iterate_selected_leaves_in_score(score)
        articulation_list = [
            marktools.Articulation(x)
            for x in articulation_list
            ]
        for leaf in leaves:
            for articulation in articulation_list:
                new_articulation = copy.copy(articulation)
                attach(new_articulation, leaf)
