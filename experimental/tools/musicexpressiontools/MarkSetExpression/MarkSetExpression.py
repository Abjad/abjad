import copy
from abjad.tools import marktools
from experimental.tools.musicexpressiontools.LeafSetExpression import LeafSetExpression


class MarkSetExpression(LeafSetExpression):
    '''Mark set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute mark set expression against `score`.
        '''
        mark = self.source_expression.payload
        assert isinstance(mark, marktools.Mark), repr(mark)
        for leaf in self._iterate_selected_leaves_in_score(score):
            new_mark = copy.deepcopy(mark)
            new_mark(leaf)
