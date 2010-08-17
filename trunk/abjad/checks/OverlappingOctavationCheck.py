from abjad.checks._Check import _Check
from abjad.tools.spannertools import OctavationSpanner


class OverlappingOctavationCheck(_Check):
   '''Octavation spanners must not overlap.'''

   def _run(self, expr):
      from abjad.tools import leaftools
      violators = [ ]
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         octavations = leaf.spanners.contained
         octavations = [p for p in octavations if isinstance(p, OctavationSpanner)]
         if 1 < len(octavations):
            for octavation in octavations:
              if octavation not in violators:
                  violators.append(octavation)
      total = [p for p in expr.spanners.contained if isinstance(p, OctavationSpanner)]
      return violators, len(total)
