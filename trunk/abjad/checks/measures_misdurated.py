from abjad.checks.check import _Check
#from abjad.helpers.instances import instances
from abjad.helpers.iterate import iterate


class MeasuresMisdurated(_Check):
   '''
   Does the (pre)prolated duration of the measure match its meter?
   '''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      #for t in instances(expr, 'Measure'):
      for t in iterate(expr, 'Measure'):
         #if t.meter is not None:
         if t.meter.forced is not None:
            #if t.duration.preprolated != t.meter.duration:
            if t.duration.preprolated != t.meter.forced.duration:
               violators.append(t)
               bad += 1
         total += 1
      return violators, total
