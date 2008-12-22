from abjad.checks.check import _Check
from abjad.helpers.hasname import hasname
#from abjad.helpers.instances import instances
from abjad.helpers.iterate import iterate


class OctavationsOverlapping(_Check):
   '''
   Octavation spanners must not overlap.
   '''

   def _run(self, expr):
      violators = [ ]
      #for leaf in instances(expr, '_Leaf'):
      for leaf in iterate(expr, '_Leaf'):
         #octavations = leaf.spanners.get(classname = 'Octavation')
         octavations = leaf.spanners.contained
         octavations = [p for p in octavations if hasname(p, 'Octavation')]
         if len(octavations) > 1:
            for octavation in octavations:
              if octavation not in violators:
                  violators.append(octavation)
      total = [p for p in expr.spanners.contained if hasname(p, 'Octavation')]
      #return violators, len(expr.spanners.get(classname = 'Octavation'))
      return violators, len(total)
