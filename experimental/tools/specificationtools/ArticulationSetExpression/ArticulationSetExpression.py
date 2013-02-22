from abjad.tools import marktools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class ArticulationSetExpression(LeafSetExpression):
    '''Articulation set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute articulation set expression against `score`.
        '''
        articulation_list = self.source_expression.payload
        leaves = self._iterate_leaves_in_score(score)
        marktools.attach_articulations_to_notes_and_chords_in_expr(leaves, articulation_list)
