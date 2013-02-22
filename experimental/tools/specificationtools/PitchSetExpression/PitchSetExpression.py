from abjad.tools import chordtools
from abjad.tools import notetools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class PitchSetExpression(LeafSetExpression):
    '''Pitch set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute pitch set expression against `score`.
        '''
        from experimental.tools import specificationtools
        if isinstance(self.source_expression, specificationtools.StatalServerCursorExpression):
            statal_server_cursor = self.source_expression.payload
        else:
            raise ValueError(self.source_expression)
        leaves = []
        for target_select_expression in self.target_select_expression_inventory:
            iterable_payload_expression = target_select_expression.evaluate_against_score(score)
            leaves.extend(iterable_payload_expression.payload)
        for leaf in leaves:
            assert isinstance(leaf, (notetools.Note, chordtools.Chord)), repr(leaf)
            chromatic_pitch_numbers = statal_server_cursor()
            assert len(chromatic_pitch_numbers) == 1
            leaf.sounding_pitch = chromatic_pitch_numbers[0]
