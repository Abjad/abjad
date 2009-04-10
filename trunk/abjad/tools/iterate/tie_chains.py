from abjad.leaf.leaf import _Leaf
from abjad.tools.iterate.naive import naive


def tie_chains(expr):
   '''Yield successive tie chains in expr.'''

   for leaf in naive(expr, _Leaf):
      if not leaf.tie.spanned or leaf.tie.last:
         yield leaf.tie.chain
