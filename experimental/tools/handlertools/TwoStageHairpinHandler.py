# -*- encoding: utf-8 -*-
import math
from abjad.tools import scoretools
from abjad.tools import marktools
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools import marktools
from abjad.tools import spannertools
from abjad.tools.scoretools import attach
from experimental.tools.handlertools.DynamicHandler import DynamicHandler


class TwoStageHairpinHandler(DynamicHandler):
    r'''Note and chord swell handler.
    '''

    ### INITIALIZER ###

    def __init__(self, swell_dynamics=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        self.swell_dynamics = swell_dynamics

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        assert len(self.swell_dynamics) == 5, repr(self.swell_dynamics)
        assert scoretools.all_are_leaves(expr), repr(expr)
        start_dynamic, left_hairpin, peak_dynamic, right_hairpin, stop_dynamic = self.swell_dynamics
        #leaves = list(iterationtools.iterate_leaves_in_expr(expr))
        #leaves = scoretools.remove_outer_rests_from_sequence(leaves)
        leaves = expr
        for leaf in iterationtools.iterate_components_in_expr(leaves):
            spanners = leaf._get_spanners(spannertools.HairpinSpanner)
            for spanner in spanners:
                spanner.detach()
        # TODO: this should eventually be changed to remove dynamic marks only
        for leaf in leaves:
            marktools.detach_lilypond_command_marks_attached_to_component(leaf)
        if 3 <= len(leaves):
            #marktools.DynamicMark(start_dynamic)(leaves[0])
            #marktools.DynamicMark(stop_dynamic)(leaves[-1])
            marktools.LilyPondCommandMark(start_dynamic, 'right')(leaves[0])
            marktools.LilyPondCommandMark(stop_dynamic, 'right')(leaves[-1])
            middle_index = int(len(leaves) / 2.0)
            middle_leaf = leaves[middle_index]
            #marktools.DynamicMark(peak_dynamic)(middle_leaf)
            marktools.LilyPondCommandMark(peak_dynamic, 'right')(middle_leaf)
            half_count = middle_index + 1
            left_leaves = leaves[:half_count]
            if len(leaves) % 2 == 0:
                right_leaves = leaves[-middle_index:]
            else:
                right_leaves = leaves[-(middle_index+1):]
            if left_hairpin == '<':
                crescendo = spannertools.CrescendoSpanner()
                attach(crescendo, left_leaves)
            else:
                decrescendo = spannertools.DecrescendoSpanner()
                attach(decrescendo, left_leaves)
            if right_hairpin == '<':
                crescendo = spannertools.CrescendoSpanner()
                attach(crescendo, right_leaves)
            else:
                decrescendo = spannertools.DecrescendoSpanner()
                attach(decrescendo, right_leaves)
            return leaves
        elif len(leaves) == 2:
            command = marktools.LilyPondCommandMark(start_dynamic, 'right')
            attach(command, leaves[0])
            command = marktools.LilyPondCommandMark(peak_dynamic, 'right')
            attach(command, leaves[-1])
            if left_hairpin == '<':
                crescendo = spannertools.CrescendoSpanner()
                attach(crescendo, leaves)
            else:
                decrescendo = spannertools.DecrescendoSpanner()
                attach(decrescendo, leaves)
        elif len(leaves) == 1:
            command = marktools.LilyPondCommandMark(peak_dynamic, 'right')
            attach(command, leaves[0])
        else:
            raise ValueError(len(leaves))

    ### PUBLIC PROPERTIES ###

    @apply
    def swell_dynamics():
        def fget(self):
            return self._swell_dynamics
        def fset(self, swell_dynamics):
            assert isinstance(swell_dynamics, (tuple, list)), repr(
                swell_dynamics)
            self._swell_dynamics = swell_dynamics
        return property(**locals())
