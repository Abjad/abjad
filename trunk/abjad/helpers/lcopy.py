from abjad.container.container import Container
from abjad.helpers.excise import excise
from abjad.helpers.iterate import iterate
from abjad.helpers.retroiterate import retroiterate
from abjad.leaf.leaf import _Leaf


def lcopy(expr, start = 0, stop = None):
   '''With stop = None, copy all leaves.'''

   # trivial leaf lcopy
   if isinstance(expr, _Leaf):
      return expr.copy( )

   # assert sequential container
   assert not expr.parallel

   # assert valid start and stop
   leaves = expr.leaves
   assert start <= len(leaves)
   if stop is None:
      stop = len(leaves)
   assert stop > start

   # find governor
   #governor = leaves[start]._parentage._governor
   governor = leaves[start].parentage._governor

   # copy governor
   governor_copy = governor.copy( )
   copy_leaves = governor_copy.leaves
   start_leaf = copy_leaves[start]
   stop_leaf = copy_leaves[stop - 1]

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
      leaf = retroiterate(governor_copy, '_Leaf').next( )
      if leaf == stop_leaf:
         _found_stop_leaf = True
      else:
         excise(leaf)

   # return trimmed governor copy
   return governor_copy
