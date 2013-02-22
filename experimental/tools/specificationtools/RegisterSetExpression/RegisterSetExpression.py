from abjad.tools import notetools
from abjad.tools import pitchtools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class RegisterSetExpression(LeafSetExpression):
    '''Register set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute register set expression against `score`.
        '''
        octave_transposition_mapping = self.source_expression.payload
        for leaf in self._iterate_leaves_in_score(score):
            assert isinstance(leaf, notetools.Note), repr(leaf)
            sounding_pitch = octave_transposition_mapping([leaf.sounding_pitch.chromatic_pitch_number])[0]
            leaf.sounding_pitch = sounding_pitch
