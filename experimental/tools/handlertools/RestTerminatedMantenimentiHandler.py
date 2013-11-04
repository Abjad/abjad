# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import datastructuretools
from abjad.tools import scoretools
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools import spannertools
from abjad.tools.functiontools import attach
from experimental.tools.handlertools.DynamicHandler import DynamicHandler


class RestTerminatedMantenimentiHandler(DynamicHandler):
    r'''Rest-terminated mantenimenti handler.
    '''

    ### INITIALIZER ###

    def __init__(self, dynamics_talea=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        dynamics_talea = dynamics_talea or []
        self.dynamics_talea = dynamics_talea

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        assert self.dynamics_talea, repr(self.dynamics_talea)
        groups = []
        classes = (scoretools.Note, scoretools.Chord)
        for i, group in enumerate(
            iterationtools.iterate_runs_in_expr(
            expr, classes)):
            spanner = spannertools.TextSpanner()
            attach(spanner, group)
            override(spanner).text_spanner.dash_fraction = 1
            dynamic_string = self.dynamics_talea[i]
            dynamic_markup = markuptools.Markup([
                markuptools.MarkupCommand('dynamic', dynamic_string),
                markuptools.MarkupCommand('hspace', 0.75)])
            override(spanner).text_spanner.bound_details__left__text = \
                dynamic_markup
            nib_markup = markuptools.Markup(
                markuptools.MarkupCommand(
                'draw-line', schemetools.SchemePair(0, 1)))
            override(spanner).text_spanner.bound_details__right__text = \
                nib_markup
            override(spanner).text_spanner.bound_details__right__padding = \
                -0.2
            override(spanner).text_spanner.bound_details__left__stencil_align_dir_y = 0
        return groups

    ### PUBLIC PROPERTIES ###

    @apply
    def dynamics_talea():
        def fget(self):
            return self._dynamics_talea
        def fset(self, dynamics_talea):
            assert isinstance(dynamics_talea, (list, tuple)), repr(
                dynamics_talea)
            self._dynamics_talea = datastructuretools.CyclicTuple(dynamics_talea)
        return property(**locals())
