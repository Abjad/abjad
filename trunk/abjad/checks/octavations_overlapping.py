from abjad.checks.check import _Check
from abjad.helpers.hasname import hasname
from abjad.helpers.iterate import iterate


class OctavationsOverlapping(_Check):
   '''Octavation spanners must not overlap.'''

   def _run(self, expr):
      from abjad.leaf.leaf import _Leaf
      violators = [ ]
      for leaf in iterate(expr, '_Leaf'):
         octavations = leaf.spanners.contained
         octavations = [p for p in octavations if hasname(p, 'Octavation')]
         if len(octavations) > 1:
            for octavation in octavations:
              if octavation not in violators:
                  violators.append(octavation)
      total = [p for p in expr.spanners.contained if hasname(p, 'Octavation')]
      return violators, len(total)
