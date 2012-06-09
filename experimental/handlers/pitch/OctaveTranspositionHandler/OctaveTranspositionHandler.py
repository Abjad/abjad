from abjad.tools import leaftools
from abjad.tools import pitchtools
from handlers.pitch.PitchHandler import PitchHandler


class OctaveTranspositionHandler(PitchHandler):

    ### INITIALIZER ###

    def __init__(self, octave_transposition_mapping):
        self.octave_transposition_mapping = \
            pitchtools.OctaveTranspositionMapping(octave_transposition_mapping)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
            if isinstance(leaf, Note):
                n = leaf.pitch.chromatic_pitch_number
                n = pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping(
                    n, self.octave_transposition_mapping)
                leaf.pitch = n
            elif isinstance(leaf, Chord):
                nn = [nh.pitch.chromatic_pitch_number for nh in leaf]
                nn = [pitchtools.transpose_chromatic_pitch_number_by_octave_transposition_mapping(
                    n, self.octave_transposition_mapping) for n in nn]
                leaf.pitches = nn
