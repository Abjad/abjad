# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.functiontools import iterate
from abjad.tools.wellformednesstools.Check import Check


class MisduratedMeasureCheck(Check):
    r'''Does the (pre)prolated duration of the measure match its
    time signature?
    '''

    def _run(self, expr):
        violators = []
        total, bad = 0, 0
        for measure in iterate(expr).by_class(scoretools.Measure):
            time_signature = measure.time_signature
            if time_signature is not None:
                if measure._preprolated_duration != time_signature.duration:
                    violators.append(measure)
                    bad += 1
            total += 1
        return violators, total
