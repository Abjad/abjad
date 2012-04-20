from abjad.tools.wellformednesstools.Check import Check


class MisfilledMeasureCheck(Check):
    '''Check that time signature duration equals measure contents duration for every measure.
    '''

    def _run(self, expr):
        from abjad.tools import componenttools
        from abjad.tools import measuretools
        violators = []
        total, bad = 0, 0
        for t in componenttools.iterate_components_forward_in_expr(expr, measuretools.Measure):
            if not t.is_full:
                violators.append(t)
                bad += 1
            total += 1
        return violators, total
