from abjad.checks.check import _Check
from abjad.helpers.hasname import hasname


class HairpinsIntermarked(_Check):
   '''
   Are there any dynamic marks in the middle of a hairpin?
   '''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      #for hairpin in expr.spanners.get(classname = '_Hairpin'):
      hairpins = [p for p in expr.spanners.contained if hasname(p, '_Hairpin')]
      for hairpin in hairpins:
         if len(hairpin.leaves) > 2:
            for leaf in hairpin.leaves[1 : -1]:
               if leaf.dynamics.mark:
                  violators.append(hairpin)
                  bad += 1
                  break
         total += 1
      return violators, total
