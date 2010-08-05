from abjad.checks._Check import _Check
from abjad.spanners import Hairpin


class IntermarkedHairpinCheck(_Check):
   '''Are there any dynamic marks in the middle of a hairpin?
   '''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      hairpins = [
         p for p in expr.spanners.contained if isinstance(p, Hairpin)]
      for hairpin in hairpins:
         if len(hairpin.leaves) > 2:
            for leaf in hairpin.leaves[1 : -1]:
               if leaf.dynamics.mark:
                  violators.append(hairpin)
                  bad += 1
                  break
         total += 1
      return violators, total
