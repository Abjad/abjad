# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import spannertools
from abjad.tools.wellformednesstools.Check import Check


class IntermarkedHairpinCheck(Check):
    r'''Are there any dynamics in the middle of a hairpin?
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        spanner_classes = (spannertools.Hairpin,)
        hairpins = expr._get_descendants()._get_spanners(spanner_classes)
        for hairpin in hairpins:
            if 2 < len(hairpin.leaves):
                for leaf in hairpin.leaves[1:-1]:
                    if leaf._get_marks(marktools.Dynamic):
                        violators.append(hairpin)
                        bad += 1
                        break
            total += 1
        return violators, total
