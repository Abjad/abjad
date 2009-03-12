from abjad.checks.check import _Check
from abjad.helpers.iterate import iterate


class MeasuresNested(_Check):
   '''Do we have any nested measures?'''

   def _run(self, expr):
      from abjad.measure.base import _Measure
      violators = [ ]
      total = 0
      for t in iterate(expr, _Measure):
         if t.parentage._first(_Measure):
               violators.append(t)
         total += 1
      return violators, total
