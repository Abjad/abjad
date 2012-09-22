from abjad.tools import contexttools
from abjad.tools import iterationtools
from abjad.tools.wellformednesstools.Check import Check


class MisduratedMeasureCheck(Check):
    '''Does the (pre)prolated duration of the measure match its meter?'''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        for measure in iterationtools.iterate_measures_in_expr(expr):
            if contexttools.get_effective_time_signature(measure) is not None:
                if measure.preprolated_duration != contexttools.get_effective_time_signature(measure).duration:
                    violators.append(measure)
                    bad += 1
            total += 1
        return violators, total
