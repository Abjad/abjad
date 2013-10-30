# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import pitchtools
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class AggregateSetExpression(LeafSetExpression):
    r'''Aggregate set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute aggregate set expression against `score`.
        '''
        aggregate = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            assert isinstance(leaf, scoretools.Note), repr(leaf)
            sounding_pitches = \
                pitchtools.register_pitch_class_numbers_by_pitch_number_aggregate(
                [leaf.sounding_pitch.pitch_number], aggregate)
            leaf.sounding_pitch = sounding_pitches[0]
