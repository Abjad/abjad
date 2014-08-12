# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class RestTerminatedMantenimentiHandler(DynamicHandler):
    r'''Rest-terminated mantenimenti handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_dynamics_talea',
        )

    ### INITIALIZER ###

    def __init__(self, dynamics_talea=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        dynamics_talea = dynamics_talea or ()
        dynamics_talea = datastructuretools.CyclicTuple(dynamics_talea)
        self._dynamics_talea = dynamics_talea

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        assert self.dynamics_talea, repr(self.dynamics_talea)
        groups = []
        classes = (scoretools.Note, scoretools.Chord)
        for i, group in enumerate(iterate(expr).by_run(classes)):
            spanner = spannertools.TextSpanner()
            attach(spanner, group)
            override(spanner).text_spanner.dash_fraction = 1
            dynamic_string = self.dynamics_talea[i]
            dynamicup = markuptools.Markup([
                markuptools.MarkupCommand('dynamic', dynamic_string),
                markuptools.MarkupCommand('hspace', 0.75)])
            override(spanner).text_spanner.bound_details__left__text = \
                dynamicup
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

    @property
    def dynamics_talea(self):
        r'''Gets dynamics talea of handler.

        Returns cyclic tuple or none.
        '''
        return self._dynamics_talea