from abjad.helpers.retroiterate import retroiterate
from abjad.helpers.spanners_detach import spanners_detach
from abjad.leaf.leaf import _Leaf


def leaves_multiply(expr, n = 1):
   '''Insert n copies of each leaf l_i after l_i in expr.
      preserve parentage and spanners.'''

   for leaf in retroiterate(expr, '_Leaf'):
      _leaf_multiply(leaf, n)
   

def _leaf_multiply(leaf, n = 1):
   '''Insert n copies of leaf after leaf.
      Preserve parentage and spanners.'''

   # assert leaf and positive number of copies
   assert isinstance(leaf, _Leaf)
   assert n > 0

   # make new leaves
   new_leaves = leaf * n

   # detach spanners from new leaves
   spanners_detach(new_leaves)
   
   # if leaf has parent
   if leaf._parent is not None:

      # find index of leaf in parent
      parent_index = leaf._parent.index(leaf)

      # insert new leaves in parent after leaf
      leaf._parent[parent_index : parent_index] = new_leaves

   # for every spanner attached to leaf
   for spanner in list(leaf.spanners.attached):

      # find index of leaf in spanner
      spanner_index = spanner.index(leaf)

      # insert new leaves in spanner after leaf
      spanner[spanner_index : spanner_index] = new_leaves
