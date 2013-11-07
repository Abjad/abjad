# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.functiontools import iterate
from abjad.tools.wellformednesstools.Check import Check


class OverlappingOctavationCheck(Check):
    r'''Octavation spanners must not overlap.
    '''

    def _run(self, expr):
        violators = []
        spanner_classes = (spannertools.OctavationSpanner, )
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            spanners = leaf._get_descendants()._get_spanners(spanner_classes)
            if 1 < len(spanners):
                for spanner in spanners:
                    if spanner not in violators:
                        violators.append(spanner)
        total = expr._get_descendants()._get_spanners(spanner_classes)
        return violators, len(total)
