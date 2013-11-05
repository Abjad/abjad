# -*- encoding: utf-8 -*-
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools.wellformednesstools.Check import Check


class MisfilledMeasureCheck(Check):
    r'''Check that time signature duration equals measure contents 
    duration for every measure.
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        for measure in iterationtools.iterate_components_in_expr(
            expr, scoretools.Measure):
            if measure.is_misfilled:
                violators.append(measure)
                bad += 1
            total += 1
        return violators, total
