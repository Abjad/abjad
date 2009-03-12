from abjad.checks.check import _Check
from abjad.helpers.iterate import iterate


class GlissandiGnashing(_Check):
   '''Glissando interface may set on 
      only last glissando spanner leaf.'''

   def _run(self, expr):
      from abjad.leaf.leaf import _Leaf
      violators =  [ ]
      for leaf in iterate(expr, _Leaf):
         if leaf.glissando:
            glissandi = leaf.glissando.spanners
            for glissando in glissandi:
               if not glissando._isMyLastLeaf(leaf):
                  violators.append(leaf)
      total = len(expr.leaves)
      return violators, total
