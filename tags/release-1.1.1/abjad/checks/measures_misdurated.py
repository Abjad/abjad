from abjad.checks.check import _Check
from abjad.tools import iterate


class MeasuresMisdurated(_Check):
   '''Does the (pre)prolated duration of the measure match its meter?'''

   def _run(self, expr):
      from abjad.measure.measure import _Measure
      violators = [ ]
      total, bad = 0, 0
      for t in iterate.naive(expr, _Measure):
         if t.meter.forced is not None:
            if t.duration.preprolated != t.meter.forced.duration:
               violators.append(t)
               bad += 1
         total += 1
      return violators, total
