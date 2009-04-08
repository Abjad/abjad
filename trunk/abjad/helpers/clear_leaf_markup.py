from abjad.tools import iterate


def clear_leaf_markup(expr):
   '''Empty t.markup.up and t.markup.down for all leaves in expr.'''

   from abjad.leaf.leaf import _Leaf
   for leaf in iterate.naive(expr, _Leaf):
      leaf.markup.up = [ ]
      leaf.markup.down = [ ]   
