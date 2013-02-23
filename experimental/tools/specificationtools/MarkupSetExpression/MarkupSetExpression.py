from abjad.tools import markuptools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class MarkupSetExpression(LeafSetExpression):
    '''Markup set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute markup set expression against `score`.
        '''
        markup = self.source_expression.payload
        for leaf in self._iterate_leaves_in_score(score):
            new_markup = markuptools.Markup(markup)
            new_markup(leaf)
