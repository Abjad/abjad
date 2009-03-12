from abjad.container.container import Container
from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.excise import excise
from abjad.helpers.iterate import iterate
from abjad.helpers.retroiterate import retroiterate
from abjad.leaf.leaf import _Leaf


def lcopy(expr, start = 0, stop = None):
   '''Copy consecutive leaves from start to stop in expr;
      copy all structure in the parentage of copied leaves,
      trimming and shrinking containers as necessary.
      
      When stop is None, copy all leaves from start in expr.'''

   # trivial leaf lcopy
   if isinstance(expr, _Leaf):
      return expr.copy( )

   # copy leaves from sequential containers only.
   if expr.parallel:
      raise ContiguityError('can not lcopy leaves from parallel container.')

   # assert valid start and stop
   leaves = expr.leaves
   assert start <= len(leaves)
   if stop is None:
      stop = len(leaves)
   assert stop > start

   # new: find start and stop leaves in expr
   start_leaf_in_expr = leaves[start]
   stop_leaf_in_expr = leaves[stop - 1]

   # find governor
   governor = leaves[start].parentage._governor

   # new: find start and stop leaves in governor
   governor_leaves = governor.leaves
   start_index_in_governor = governor_leaves.index(start_leaf_in_expr)
   stop_index_in_governor = governor_leaves.index(stop_leaf_in_expr)

   # copy governor
   governor_copy = governor.copy( )
   copy_leaves = governor_copy.leaves
   #start_leaf = copy_leaves[start]
   #stop_leaf = copy_leaves[stop - 1]

   # new: find start and stop leaves in copy of governor
   start_leaf = copy_leaves[start_index_in_governor]
   stop_leaf = copy_leaves[stop_index_in_governor]

   #print start_leaf, stop_leaf
   #print ''

   # trim governor copy forwards from first leaf
   _found_start_leaf = False

   while not _found_start_leaf:
      leaf = iterate(governor_copy, '_Leaf').next( )
      if leaf == start_leaf:
         _found_start_leaf = True
      else:
         excise(leaf)

   #print 'moved on to trimming backwards ...'

   # trim governor copy backwards from last leaf
   _found_stop_leaf = False

   while not _found_stop_leaf:
      #leaf = retroiterate(governor_copy, '_Leaf').next( )
      leaf = retroiterate(governor_copy, _Leaf).next( )
      if leaf == stop_leaf:
         _found_stop_leaf = True
      else:
         excise(leaf)

   # return trimmed governor copy
   return governor_copy
