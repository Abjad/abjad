import math
from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import marktools
from abjad.tools import spannertools
from experimental.tools.handlertools.DynamicHandler import DynamicHandler


class TwoStageHairpinHandler(DynamicHandler):
    '''Note and chord swell handler.
    '''

    ### INITIALIZER ###

    def __init__(self, swell_dynamics=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        self.swell_dynamics = swell_dynamics

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        assert len(self.swell_dynamics) == 5, repr(self.swell_dynamics)
        assert leaftools.all_are_leaves(expr), repr(expr)
        start_dynamic, left_hairpin, peak_dynamic, right_hairpin, stop_dynamic = self.swell_dynamics
        #leaves = list(iterationtools.iterate_leaves_in_expr(expr))
        #leaves = leaftools.remove_outer_rests_from_sequence(leaves)
        leaves = expr
        if 3 <= len(leaves):
            #contexttools.DynamicMark(start_dynamic)(leaves[0])
            #contexttools.DynamicMark(stop_dynamic)(leaves[-1])
            marktools.LilyPondCommandMark(start_dynamic, 'right')(leaves[0])
            marktools.LilyPondCommandMark(stop_dynamic, 'right')(leaves[-1])
            middle_index = int(len(leaves) / 2.0)
            middle_leaf = leaves[middle_index]
            #contexttools.DynamicMark(peak_dynamic)(middle_leaf)
            marktools.LilyPondCommandMark(peak_dynamic, 'right')(middle_leaf)
            half_count = middle_index + 1
            left_leaves = leaves[:half_count]
            if len(leaves) % 2 == 0:
                right_leaves = leaves[-middle_index:]
            else:
                right_leaves = leaves[-(middle_index+1):]
            if left_hairpin == '<':
                spannertools.CrescendoSpanner(left_leaves)
            else:
                spannertools.DecrescendoSpanner(left_leaves)
            if right_hairpin == '<':
                spannertools.CrescendoSpanner(right_leaves)
            else:
                spannertools.DecrescendoSpanner(right_leaves)
            return leaves

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def swell_dynamics():
        def fget(self):
            return self._swell_dynamics
        def fset(self, swell_dynamics):
            assert isinstance(swell_dynamics, (tuple, list)), repr(swell_dynamics)
            self._swell_dynamics = swell_dynamics
        return property(**locals())
