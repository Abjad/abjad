# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.handlertools.ArticulationHandler import ArticulationHandler


class RepeatedMarkupHandler(ArticulationHandler):
    r'''Repeated markup handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_markups',
        )

    ### INITIALIZER ###

    def __init__(self, markups=None):
        if markups is not None:
            markups = [markuptools.Markup(_) for _ in markups]
            markups = tuple(markups)
        self._markups = markups

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        classes = (scoretools.Note, scoretools.Chord)
        markups = datastructuretools.CyclicTuple(self.markups)
        for i, leaf in  enumerate(
            scoretools.iterate_components_forward_in_expr(expr, classes)):
            markup = markup[i]
            markup = markuptools.Markup(markup)
            markup(leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def markups(self):
        r'''Gets markups of handler.

        Returns tuple or none.
        '''
        return self._markups