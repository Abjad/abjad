# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from experimental.tools.handlertools.ArticulationHandler \
    import ArticulationHandler


class StemTremoloHandler(ArticulationHandler):

    ### INITIALIZER ###

    def __init__(self, hash_mark_counts):
        self.hash_mark_counts = hash_mark_counts

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        classes = (scoretools.Note, scoretools.Chord)
        hash_mark_counts = datastructuretools.CyclicTuple(self.hash_mark_counts)
        for i, leaf in enumerate(
            scoretools.iterate_components_forward_in_expr(expr, classes)):
            marktools.StemTremolo(hash_mark_counts[i])(leaf)
