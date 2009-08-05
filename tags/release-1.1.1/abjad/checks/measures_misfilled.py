from abjad.checks.check import _Check
from abjad.tools import iterate


class MeasuresImproperlyFilled(_Check):
   '''For each (rigid) measure, 
      does effective meter duration equal preprolated duration?'''

   def _run(self, expr):
      #from abjad.measure import RigidMeasure
      from abjad.measure import RigidMeasure
      violators = [ ]
      total, bad = 0, 0
      for t in iterate.naive(expr, RigidMeasure):
         if not t.full:
            violators.append(t)
            bad += 1
         total += 1
      return violators, total
