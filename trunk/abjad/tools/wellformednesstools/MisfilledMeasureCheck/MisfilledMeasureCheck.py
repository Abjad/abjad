from abjad.tools import componenttools
from abjad.tools import measuretools
from abjad.tools.wellformednesstools.Check import Check


class MisfilledMeasureCheck(Check):
    '''Check that time signature duration equals measure contents duration for every measure.
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        for measure in componenttools.iterate_components_forward_in_expr(expr, measuretools.Measure):
            if measure.is_misfilled:
                violators.append(measure)
                bad += 1
            total += 1
        return violators, total
