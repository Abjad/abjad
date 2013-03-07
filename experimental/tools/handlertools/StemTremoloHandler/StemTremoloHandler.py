from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import sequencetools
from experimental.tools.handlertools.ArticulationHandler import ArticulationHandler


class StemTremoloHandler(ArticulationHandler):

    ### INITIALIZER ###

    def __init__(self, hash_mark_counts):
        self.hash_mark_counts = hash_mark_counts

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        classes = (notetools.Note, chordtools.Chord)
        hash_mark_counts = sequencetools.CyclicTuple(self.hash_mark_counts)
        for i, leaf in enumerate(componenttools.iterate_components_forward_in_expr(expr, classes)):
            marktools.StemTremolo(hash_mark_counts[i])(leaf)
