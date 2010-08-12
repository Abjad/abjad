from abjad.checks._Check import _Check
from abjad.spanners import GlissandoSpanner


class OverlappingGlissandoCheck(_Check):
   '''Glissandi must not overlap.
   Dove-tailed glissandi are OK.'''

   def _run(self, expr):
      from abjad.tools import leaftools
      violators = [ ] 
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         glissandi = leaf.glissando.spanners
         if 1 < len(glissandi):
            if len(glissandi) == 2:
               common_leaves = set(glissandi[0].leaves) & \
                  set(glissandi[1].leaves)
               if len(common_leaves) == 1:
                  x = list(common_leaves)[0]
                  if (glissandi[0]._is_my_first_leaf(x) and 
                     glissandi[1]._is_my_last_leaf(x)) or \
                     (glissandi[1]._is_my_first_leaf(x) and 
                      glissandi[0]._is_my_last_leaf(x)):
                     break  

            for glissando in glissandi:
               if glissando not in violators:
                  violators.append(glissando)
      total = [p for p in expr.spanners.contained if isinstance(p, GlissandoSpanner)]
      return violators, len(total)
