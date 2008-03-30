from abjad.checks.check import _Check
from abjad.helpers.instances import instances


class MeasuresNested(_Check):
   '''Do we have any nested measures?'''

   def _run(self, expr):
      violators = [ ]
      total = 0
      for t in instances(expr, 'Measure'):
         if t._parentage._first('Measure'):
               violators.append(t)
         total += 1
      return violators, total
