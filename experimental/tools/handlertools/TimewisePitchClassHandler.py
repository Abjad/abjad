# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from experimental.tools.handlertools.PitchHandler import PitchHandler


class TimewisePitchClassHandler(PitchHandler):

    ### INITIALIZER ###

    def __init__(self, pitch_class_server):
        self.pitch_class_server = pitch_class_server

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        classes = (scoretools.Note, scoretools.Chord)
        for leaf in \
            scoretools.iterate_components_forward_in_expr(expr, classes):
            if isinstance(leaf, scoretools.Note):
                pitch_class = \
                    self.pitch_class_server.get_next_n_nodes_at_level(1, -1)
                leaf.written_pitch = pitch_class
            elif isinstance(leaf, scoretools.Chord):
                pitch_classes = \
                    self.pitch_class_server.get_next_n_nodes_at_level(
                        len(leaf), -1)
                leaf.clear()
                leaf.extend(pitch_classes)
            else:
                raise ValueError
