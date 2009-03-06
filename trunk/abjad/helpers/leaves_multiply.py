from abjad.helpers.retroiterate import retroiterate
from abjad.helpers.spanners_detach import spanners_detach
from abjad.helpers.splice_after import splice_after
from abjad.leaf.leaf import _Leaf


def leaves_multiply(expr, total = 1):
   '''Insert n copies of each leaf l_i after l_i in expr.
      preserve parentage and spanners.'''

   for leaf in retroiterate(expr, '_Leaf'):
      _leaf_multiply(leaf, total)
   

def _leaf_multiply(leaf, total = 1):
   '''Insert n copies of leaf after leaf.
      Preserve parentage and spanners.'''

   assert isinstance(leaf, _Leaf)
   assert total > 0

   new_leaves = leaf * (total - 1)
   spanners_detach(new_leaves, level = 'all')
   splice_after(leaf, new_leaves)
