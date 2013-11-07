# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.functiontools import iterate
from abjad.tools.wellformednesstools.Check import Check


class OverlappingGlissandoCheck(Check):
    r'''Glissandi must not overlap.
    Dove-tailed glissandi are OK.
    '''

    def _run(self, expr):
        violators = []
        spanner_classes = (spannertools.GlissandoSpanner,)
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            glissandi = leaf._get_spanners(spanner_classes)
            if 1 < len(glissandi):
                if len(glissandi) == 2:
                    common_leaves = set(glissandi[0].leaves) & \
                        set(glissandi[1].leaves)
                    if len(common_leaves) == 1:
                        x = list(common_leaves)[0]
                        if (glissandi[0]._is_my_first_leaf(x) and
                            glissandi[1]._is_my_last_leaf(x)) or \
                            (glissandi[1]._is_my_first_leaf(x) and
                            glissandi[0]._is_my_last_leaf(x)):
                            break

                for glissando in glissandi:
                    if glissando not in violators:
                        violators.append(glissando)
        total = expr._get_descendants()._get_spanners(spanner_classes)
        return violators, len(total)
