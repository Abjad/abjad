# -*- encoding: utf-8 -*-
import math
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class TwoStageHairpinHandler(DynamicHandler):
    r'''Two-stage hairpin handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_swell_dynamics',
        )

    ### INITIALIZER ###

    def __init__(self, swell_dynamics=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if swell_dynamics is not None:
            swell_dynamic = tuple(swell_dynamics)
        self._swell_dynamics = swell_dynamics

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        assert len(self.swell_dynamics) == 5, repr(self.swell_dynamics)
        assert scoretools.all_are_leaves(expr), repr(expr)
        start_dynamic, left_hairpin, peak_dynamic, right_hairpin, stop_dynamic = self.swell_dynamics
        #leaves = list(iterate(expr).by_class(scoretools.Leaf))
        #leaves = scoretools.remove_outer_rests_from_sequence(leaves)
        leaves = expr
        for leaf in iterate(leaves).by_class():
            spanners = leaf._get_spanners(spannertools.Hairpin)
            for spanner in spanners:
                spanner.detach()
        # TODO: this should eventually be changed to remove dynamics only
        for leaf in leaves:
            indicatortools.detach_lilypond_commands_attached_to_component(leaf)
        if 3 <= len(leaves):
            #indicatortools.Dynamic(start_dynamic)(leaves[0])
            #indicatortools.Dynamic(stop_dynamic)(leaves[-1])
            indicatortools.LilyPondCommand(start_dynamic, 'right')(leaves[0])
            indicatortools.LilyPondCommand(stop_dynamic, 'right')(leaves[-1])
            middle_index = int(len(leaves) / 2.0)
            middle_leaf = leaves[middle_index]
            #indicatortools.Dynamic(peak_dynamic)(middle_leaf)
            indicatortools.LilyPondCommand(peak_dynamic, 'right')(middle_leaf)
            half_count = middle_index + 1
            left_leaves = leaves[:half_count]
            if len(leaves) % 2 == 0:
                right_leaves = leaves[-middle_index:]
            else:
                right_leaves = leaves[-(middle_index+1):]
            if left_hairpin == '<':
                crescendo = spannertools.Crescendo()
                attach(crescendo, left_leaves)
            else:
                decrescendo = spannertools.Decrescendo()
                attach(decrescendo, left_leaves)
            if right_hairpin == '<':
                crescendo = spannertools.Crescendo()
                attach(crescendo, right_leaves)
            else:
                decrescendo = spannertools.Decrescendo()
                attach(decrescendo, right_leaves)
            return leaves
        elif len(leaves) == 2:
            command = indicatortools.LilyPondCommand(start_dynamic, 'right')
            attach(command, leaves[0])
            command = indicatortools.LilyPondCommand(peak_dynamic, 'right')
            attach(command, leaves[-1])
            if left_hairpin == '<':
                crescendo = spannertools.Crescendo()
                attach(crescendo, leaves)
            else:
                decrescendo = spannertools.Decrescendo()
                attach(decrescendo, leaves)
        elif len(leaves) == 1:
            command = indicatortools.LilyPondCommand(peak_dynamic, 'right')
            attach(command, leaves[0])
        else:
            raise ValueError(len(leaves))

    ### PUBLIC PROPERTIES ###

    @property
    def swell_dynamics(self):
        r'''Gets swell dynamics of handler.

        Returns tuple of strings or none.
        '''
        return self._swell_dynamics