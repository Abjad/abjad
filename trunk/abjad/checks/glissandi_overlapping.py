from abjad.checks.check import _Check
from abjad.helpers.instances import instances


class GlissandiOverlapping(_Check):
   '''Glissandi must not overlap.
      Dove-tailed glissandi are OK.'''

   def _run(self, expr):
      violators = [ ] 
      for leaf in instances(expr, '_Leaf'):
         glissandi = leaf.glissando.spanners
         if len(glissandi) > 1:
            if len(glissandi) == 2:
               common_leaves = set(glissandi[0].leaves) & \
                  set(glissandi[1].leaves)
               if len(common_leaves) == 1:
                  x = list(common_leaves)[0]
                  if (glissandi[0]._isMyFirstLeaf(x) and 
                     glissandi[1]._isMyLastLeaf(x)) or \
                     (glissandi[1]._isMyFirstLeaf(x) and 
                      glissandi[0]._isMyLastLeaf(x)):
                     break  

            for glissando in glissandi:
               if glissando not in violators:
                  violators.append(glissando)
      return violators, len(expr.spanners.get(classname = 'Glissando'))
