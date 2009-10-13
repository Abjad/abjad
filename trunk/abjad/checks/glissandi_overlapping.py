from abjad.checks.check import _Check
from abjad.leaf.leaf import _Leaf
from abjad.tools import iterate
from abjad.spanners.glissando import Glissando


class GlissandiOverlapping(_Check):
   '''Glissandi must not overlap.
      Dove-tailed glissandi are OK.'''

   def _run(self, expr):
      #from abjad.glissando import Glissando
      #from abjad.leaf.leaf import _Leaf
      violators = [ ] 
      for leaf in iterate.naive(expr, _Leaf):
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
      total = [p for p in expr.spanners.contained if isinstance(p, Glissando)]
      return violators, len(total)
