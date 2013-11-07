# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate
from abjad.tools.wellformednesstools.Check import Check


class MisfilledMeasureCheck(Check):
    r'''Check that time signature duration equals measure contents
    duration for every measure.
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        for measure in iterate(expr).by_class(scoretools.Measure):
            if measure.is_misfilled:
                violators.append(measure)
                bad += 1
            total += 1
        return violators, total
