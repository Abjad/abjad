from abjad.checks.check import _Check
#from abjad.helpers.instances import instances
from abjad.helpers.iterate import iterate


class MeasuresNested(_Check):
   '''
   Do we have any nested measures?
   '''

   def _run(self, expr):
      violators = [ ]
      #for t in instances(expr, 'Measure'):
      total = 0
      for t in iterate(expr, 'Measure'):
         if t._parentage._first('Measure'):
               violators.append(t)
         total += 1
      return violators, total
