from abjad.checks.check import _Check
from abjad.measure import _Measure
from abjad.tools import iterate


class MeasuresNested(_Check):
   '''Do we have any nested measures?'''

   def _run(self, expr):
      from abjad.tools import parenttools
      violators = [ ]
      total = 0
      for t in iterate.measures_forward_in_expr(expr):
         if parenttools.get_first(t, _Measure):
            violators.append(t)
         total += 1
      return violators, total
