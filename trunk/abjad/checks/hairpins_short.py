from abjad.checks.check import _Check
from abjad.helpers.hasname import hasname


class HairpinsShort(_Check):
   '''
   Hairpins must span at least two leaves.
   '''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      #for hairpin in expr.spanners.get(classname = '_Hairpin'):
      hairpins = [p for p in expr.spanners.contained if hasname(p, '_Hairpin')]
      for hairpin in hairpins:
         if len(hairpin.leaves) <= 1:
            violators.append(hairpin)
         total += 1
      return violators, total
