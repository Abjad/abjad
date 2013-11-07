# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate
from abjad.tools.wellformednesstools.Check import Check


class NestedMeasureCheck(Check):
    r'''Do we have any nested measures?
    '''

    def _run(self, expr):
        violators = []
        total = 0
        for measure in iterate(expr).by_class(scoretools.Measure):
            parentage = measure._get_parentage(include_self=False)
            if parentage.get_first(scoretools.Measure):
                violators.append(measure)
            total += 1
        return violators, total
