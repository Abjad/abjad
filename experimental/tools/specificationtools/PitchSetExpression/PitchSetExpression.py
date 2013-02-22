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
        statal_server_cursor = self.source_expression.payload
        leaves = []
        for leaf in self._iterate_leaves_in_score(score):
            assert isinstance(leaf, (notetools.Note, chordtools.Chord)), repr(leaf)
            chromatic_pitch_numbers = statal_server_cursor()
            assert len(chromatic_pitch_numbers) == 1
            leaf.sounding_pitch = chromatic_pitch_numbers[0]
