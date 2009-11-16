from abjad.checks.check import _Check
from abjad.spanners import Octavation
from abjad.tools import iterate


class OctavationsOverlapping(_Check):
   '''Octavation spanners must not overlap.'''

   def _run(self, expr):
      violators = [ ]
      for leaf in iterate.leaves_forward_in(expr):
         octavations = leaf.spanners.contained
         octavations = [p for p in octavations if isinstance(p, Octavation)]
         if len(octavations) > 1:
            for octavation in octavations:
              if octavation not in violators:
                  violators.append(octavation)
      total = [p for p in expr.spanners.contained if isinstance(p, Octavation)]
      return violators, len(total)
