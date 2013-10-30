# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import markuptools
from abjad.tools import scoretools
from experimental.tools.handlertools.ArticulationHandler \
    import ArticulationHandler


class RepeatedMarkupHandler(ArticulationHandler):

    ### INITIALIZER ###

    def __init__(self, markups):
        self.markups = markups

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        classes = (scoretools.Note, scoretools.Chord)
        markups = datastructuretools.CyclicTuple(self.markups)
        for i, leaf in  enumerate(
            scoretools.iterate_components_forward_in_expr(expr, classes)):
            markup = markup[i]
            markup = markuptools.Markup(markup)
            markup(leaf)
