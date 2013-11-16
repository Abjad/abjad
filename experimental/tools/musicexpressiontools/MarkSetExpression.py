# -*- encoding: utf-8 -*-
import copy
from abjad.tools import indicatortools
from abjad.tools.topleveltools import attach
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class MarkSetExpression(LeafSetExpression):
    r'''Mark set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute mark set expression against `score`.
        '''
        mark = self.source_expression.payload
        #assert isinstance(mark, indicatortools.Mark), repr(mark)
        for leaf in self._iterate_selected_leaves_in_score(score):
            new_mark = copy.deepcopy(mark)
            attach(new_mark, leaf)
