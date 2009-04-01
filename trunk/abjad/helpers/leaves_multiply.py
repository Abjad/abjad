from abjad.helpers.retroiterate import retroiterate
from abjad.helpers.withdraw_from_attached_spanners import \
   _withdraw_from_attached_spanners
from abjad.leaf.leaf import _Leaf


def leaves_multiply(expr, total = 1):
   '''Insert n copies of each leaf l_i after l_i in expr.
      preserve parentage and spanners.'''

   for leaf in retroiterate(expr, _Leaf):
      print 'debug: leaf %s' % leaf
      _leaf_multiply(leaf, total)
   

def _leaf_multiply(leaf, total = 1):
   '''Insert n copies of leaf after leaf.
      Preserve parentage and spanners.'''

   assert isinstance(leaf, _Leaf)
   assert total > 0

   new_leaves = leaf * (total - 1)
   _withdraw_from_attached_spanners(new_leaves)
   leaf.splice(new_leaves)
