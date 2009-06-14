from abjad.container import Container
from abjad.exceptions import ContiguityError
from abjad.leaf.leaf import _Leaf
from abjad.tools import leaftools
from abjad.tools import iterate
from abjad.tools.clone.fracture import fracture


def by_leaf_range_with_parentage(expr, start = 0, stop = None):
   '''Copy consecutive leaves from start to stop in expr.
      Copy all structure in the parentage of copied leaves.
      Trim and shrink parent containers as necessary.
      When stop is None, copy all leaves from start in expr.'''

   # trivial leaf lcopy
   if isinstance(expr, _Leaf):
      return fracture([expr])[0]

   # copy leaves from sequential containers only.
   if expr.parallel:
      raise ContiguityError('can not lcopy leaves from parallel container.')

   # assert valid start and stop
   leaves = expr.leaves
   assert start <= len(leaves)
   if stop is None:
      stop = len(leaves)
   assert start < stop

   # new: find start and stop leaves in expr
   start_leaf_in_expr = leaves[start]
   stop_leaf_in_expr = leaves[stop - 1]

   # find governor
   governor = leaves[start].parentage.governor

   # new: find start and stop leaves in governor
   governor_leaves = governor.leaves
   start_index_in_governor = governor_leaves.index(start_leaf_in_expr)
   stop_index_in_governor = governor_leaves.index(stop_leaf_in_expr)

   # copy governor
   governor_copy = fracture([governor])[0]
   copy_leaves = governor_copy.leaves

   # new: find start and stop leaves in copy of governor
   start_leaf = copy_leaves[start_index_in_governor]
   stop_leaf = copy_leaves[stop_index_in_governor]

   # trim governor copy forwards from first leaf
   _found_start_leaf = False

   while not _found_start_leaf:
      leaf = iterate.naive(governor_copy, _Leaf).next( )
      if leaf == start_leaf:
         _found_start_leaf = True
      else:
         leaftools.excise(leaf)

   #print 'moved on to trimming backwards ...'

   # trim governor copy backwards from last leaf
   _found_stop_leaf = False

   while not _found_stop_leaf:
      leaf = iterate.backwards(governor_copy, _Leaf).next( )
      if leaf == stop_leaf:
         _found_stop_leaf = True
      else:
         leaftools.excise(leaf)

   # return trimmed governor copy
   return governor_copy
