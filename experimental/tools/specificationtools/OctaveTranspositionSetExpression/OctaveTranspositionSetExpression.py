from abjad.tools import notetools
from abjad.tools import pitchtools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class OctaveTranspositionSetExpression(LeafSetExpression):
    '''Octave transposition set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute octave transposition set expression against `score`.
        '''
        from experimental.tools import specificationtools
        octave_transposition_mapping = self.source_expression.payload
        leaves = []
        for target_select_expression in self.target_select_expression_inventory:
            iterable_payload_expression = target_select_expression.evaluate_against_score(score)
            leaves.extend(iterable_payload_expression.payload)
        for leaf in leaves:
            assert isinstance(leaf, notetools.Note), repr(leaf)
            sounding_pitch = octave_transposition_mapping([leaf.sounding_pitch.chromatic_pitch_number])[0]
            leaf.sounding_pitch = sounding_pitch
