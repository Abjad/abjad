# -*- encoding: utf-8 -*-
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class ShortHairpinCheck(Check):
    r'''Hairpins must span at least two leaves.
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        spanner_classes = (spannertools.HairpinSpanner,)
        hairpins = expr._get_descendants()._get_spanners(spanner_classes)
        for hairpin in hairpins:
            if len(hairpin.leaves) <= 1:
                violators.append(hairpin)
            total += 1
        return violators, total
