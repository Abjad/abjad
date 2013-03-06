from abjad.tools import notetools
from abjad.tools import pitchtools
from experimental.tools.specificationtools.LeafSetExpression import LeafSetExpression


class AggregateSetExpression(LeafSetExpression):
    '''Aggregate set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        '''Execute aggregate set expression against `score`.
        '''
        aggregate = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            assert isinstance(leaf, notetools.Note), repr(leaf)
            sounding_pitches = \
                pitchtools.register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate(
                [leaf.sounding_pitch.chromatic_pitch_number], aggregate)
            leaf.sounding_pitch = sounding_pitches[0]
