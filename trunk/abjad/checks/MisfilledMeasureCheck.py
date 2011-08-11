from abjad.checks._Check import _Check


class MisfilledMeasureCheck(_Check):
    '''For each (rigid) measure,
    does effective meter duration equal preprolated duration?
    '''

    def _run(self, expr):
        from abjad.tools import componenttools
        from abjad.tools.measuretools.Measure import Measure
        violators = [ ]
        total, bad = 0, 0
        for t in componenttools.iterate_components_forward_in_expr(expr, Measure):
            if not t.is_full:
                violators.append(t)
                bad += 1
            total += 1
        return violators, total
