from abjad.tools import chordtools
from abjad.tools import componenttools
from abjad.tools import markuptools
from abjad.tools import notetools
from experimental.tools.handlertools.articulations.ArticulationHandler import ArticulationHandler


class RepeatedMarkupHandler(ArticulationHandler):

    ### INITIALIZER ###

    def __init__(self, markups):
        self.markups = markups

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        classes = (notetools.Note, chordtools.Chord)
        markups = sequencetools.CyclicTuple(self.markups)
        for i, leaf in enumerate(componenttools.iterate_components_forward_in_expr(expr, classes)):
            markup = markup[i]
            markup = markuptools.Markup(markup)
            markup(leaf)
