from abjad.checks.check import _Check
from abjad.spanners import Hairpin


class HairpinsShort(_Check):
   '''Hairpins must span at least two leaves.
   '''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      hairpins = [
         p for p in expr.spanners.contained if isinstance(p, Hairpin)]
      for hairpin in hairpins:
         if len(hairpin.leaves) <= 1:
            violators.append(hairpin)
         total += 1
      return violators, total
