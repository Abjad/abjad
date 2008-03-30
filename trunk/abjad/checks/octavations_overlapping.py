from abjad.checks.check import _Check
from abjad.helpers.instances import instances


class OctavationsOverlapping(_Check):
   '''Octavation spanners must not overlap.'''

   def _run(self, expr):
      violators = [ ]
      for leaf in instances(expr, '_Leaf'):
         octavations = leaf.spanners.get(classname = 'Octavation')
         if len(octavations) > 1:
            for octavation in octavations:
               if octavation not in violators:
                  violators.append(octavation)
      return violators, len(expr.spanners.get(classname = 'Octavation'))
