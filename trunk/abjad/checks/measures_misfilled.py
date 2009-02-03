from abjad.checks.check import _Check
from abjad.helpers.iterate import iterate


class MeasuresMisfilled(_Check):
   '''
   For each (rigid) measure, 
   does effective meter duration equal contents duration?
   '''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      for t in iterate(expr, 'RigidMeasure'):
         if not t.full:
            violators.append(t)
            bad += 1
         total += 1
      return violators, total
