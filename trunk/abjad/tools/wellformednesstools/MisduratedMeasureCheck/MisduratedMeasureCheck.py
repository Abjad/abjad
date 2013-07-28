from abjad.tools import contexttools
from abjad.tools import iterationtools
from abjad.tools.wellformednesstools.Check import Check


class MisduratedMeasureCheck(Check):
    '''Does the (pre)prolated duration of the measure match its 
    time signature?
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        for measure in iterationtools.iterate_measures_in_expr(expr):
            time_signature = measure.get_effective_context_mark(
                contexttools.TimeSignatureMark)
            if time_signature is not None:
                if measure._preprolated_duration != time_signature.duration:
                    violators.append(measure)
                    bad += 1
            total += 1
        return violators, total
