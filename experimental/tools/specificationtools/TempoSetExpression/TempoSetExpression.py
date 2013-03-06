from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class TempoSetExpression(LeafSetExpression):
    '''Tempo set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute tempo set expression against `score`.
        '''
        tempo_mark = self.source_expression.payload
        first_leaf = self._iterate_selected_leaves_in_score(score)[0]
        tempo_mark(first_leaf)
