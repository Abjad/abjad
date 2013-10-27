# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import spannertools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class IntermarkedHairpinCheck(Check):
    r'''Are there any dynamic marks in the middle of a hairpin?
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        spanner_classes = (spannertools.HairpinSpanner,)
        hairpins = expr._get_descendants()._get_spanners(spanner_classes)
        for hairpin in hairpins:
            if 2 < len(hairpin.leaves):
                for leaf in hairpin.leaves[1:-1]:
                    if leaf._get_marks(contexttools.DynamicMark):
                        violators.append(hairpin)
                        bad += 1
                        break
            total += 1
        return violators, total
