from abjad.checks._Check import _Check
from abjad.components._Measure import _Measure


class NestedMeasureCheck(_Check):
   '''Do we have any nested measures?'''

   def _run(self, expr):
      from abjad.tools import measuretools
      from abjad.tools import componenttools
      violators = [ ]
      total = 0
      for t in measuretools.iterate_measures_forward_in_expr(expr):
         if componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
            t, _Measure):
            violators.append(t)
         total += 1
      return violators, total
