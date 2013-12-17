# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.agenttools.InspectionAgent import inspect
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression


class RegisterSetExpression(LeafSetExpression):
    r'''Register set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute register set expression against `score`.
        '''
        octave_transposition_mapping = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            assert isinstance(leaf, scoretools.Note), repr(leaf)
            leaf_sounding_pitch = inspect(leaf).get_sounding_pitch()
            sounding_pitches = octave_transposition_mapping(
                [leaf_sounding_pitch.pitch_number])
            sounding_pitch = sounding_pitches[0]
            #leaf.sounding_pitch = sounding_pitch
            # TODO: FIXME
            leaf.written_pitch = sounding_pitch
