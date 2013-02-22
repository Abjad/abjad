from abjad.tools import marktools
from experimental.tools.specificationtools.GeneralizedSetExpression import GeneralizedSetExpression


class ArticulationSetExpression(GeneralizedSetExpression):
    '''Articulation set expression.
    '''

    ### INITIALIZER ###

    def __init__(self, source_expression=None, target_select_expression_inventory=None):
        GeneralizedSetExpression.__init__(self, attribute='note_head_color',
            source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory)

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute articulation set expression against `score`.
        '''
        from experimental.tools import specificationtools
        articulation_list = self.source_expression.payload
        leaves = []
        for target_select_expression in self.target_select_expression_inventory:
            iterable_payload_expression = target_select_expression.evaluate_against_score(score)
            leaves.extend(iterable_payload_expression.payload)
        marktools.attach_articulations_to_notes_and_chords_in_expr(leaves, articulation_list)
