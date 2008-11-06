from abjad.checks.check import _Check
from abjad.helpers.instances import instances


class MeasuresMisdurated(_Check):
   '''Does the (pre)prolated duration of the measure match its meter?'''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      for t in instances(expr, 'Measure'):
         if t.meter is not None:
            if t.duration.preprolated != t.meter.duration:
               violators.append(t)
               bad += 1
         total += 1
      return violators, total
