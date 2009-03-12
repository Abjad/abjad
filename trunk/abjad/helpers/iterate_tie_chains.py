from abjad.helpers.iterate import iterate


def iterate_tie_chains(expr):
   '''Yield successive tie chains in expr.'''

   from abjad.leaf.leaf import _Leaf
   for leaf in iterate(expr, _Leaf):
      if not leaf.tie.spanned or leaf.tie.last:
         yield leaf.tie.chain
