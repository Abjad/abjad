from abjad.tools import labeltools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class NoteHeadColorSetExpression(LeafSetExpression):
    '''Note head color set expression.
    '''    

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute note head color set expression against `score`.
        '''
        from experimental.tools import specificationtools
        color = self.source_expression.payload
        leaves = []
        for target_select_expression in self.target_select_expression_inventory:
            iterable_payload_expression = target_select_expression.evaluate_against_score(score)
            leaves.extend(iterable_payload_expression.payload)
        for leaf in leaves:
            labeltools.color_leaf(leaf, color)
            leaf.override.beam.color = color
            leaf.override.flag.color = color
            leaf.override.stem.color = color
