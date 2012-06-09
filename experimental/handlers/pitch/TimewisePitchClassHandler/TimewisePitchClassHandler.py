from abjad.tools import componenttools
from experimental.handlers.pitch.PitchHandler import PitchHandler


class TimewisePitchClassHandler(PitchHandler):

    ### INITIALIZER ###

    def __init__(self, pitch_class_server):
        self.pitch_class_server = pitch_class_server

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        klasses = (notetools.Note, chordtools.Chord)
        for leaf in componenttools.iterate_components_forward_in_expr(expr, klasses):
            if isinstance(leaf, notetools.Note):
                pitch_class = self.pitch_class_server.get_next_n_nodes_at_level(1, -1)
                leaf.written_pitch = pitch_class
            elif isinstance(leaf, chordtools.Chord):
                pitch_classes = self.pitch_class_server.get_next_n_nodes_at_level(len(leaf), -1)
                leaf.clear()
                leaf.extend(pitch_classes)
            else:
                raise ValueError
