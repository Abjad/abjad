from abjad.containers.container import Container
from abjad.leaf.leaf import _Leaf

# lcopy(t, 5, 7)
def lcopy(expr, start = 0, stop = float('inf')):
   '''
   With stop = None, copy all leaves.

   # pseudocode:

   # get start leaf
   # find governor of whole damn thing
   # copy governor (while ignoring any parent, parallel containers 
   # which enclose governor)
   # trim shit in governor copy before start leaf
   # trim shit in governor copy after stop leaf
   # return 'trimmed' governor copy
   '''

   # trivial leaf lcopy
   if isinstance(expr, _Leaf):
      return expr.copy( )

   # assert valid start and stop
   leaves = expr.leaves
   assert start <= len(leaves)
   assert stop > start or stop is None

   # find governor
   governor = leaves[start]._parentage._governor

   # copy governor
   governor_copy = governor.copy( )
   copy_leaves = governor_copy.leaves
   start_leaf = copy_leaves[start]
   stop_leaf = copy_leaves[stop]

   # trim governor copy
#   for i, leaf in enumerate(governor_copy.leaves):
#      if i < start or i > stop:
#         _trim(leaf, governor_copy)

   _found_start_leaf = False

   while not _found_start_leaf:
      leaf = iterate(governor_copy, '_Leaf').next( )
      if leaf == start_leaf:
         _found_start_leaf = True
      else:
         if leaf._parent != start_leaf._parent:
            del(leaf._parent)
         else:
            del(leaf)

   # return trimmed governor copy
   return governor_copy


def _trim(leaf, governor_reference):
   '''Is leaf last in any containers in parentage?
      If so, delete empty container;
      if not, don't both;
      finally, delete leaf.
   '''

   while True:
      parent = leaf._parent
      #del(leaf)
      parent.trim(leaf) or parent.trim(0) # can't remember trim syntax
      if not len(parent):
         parent = leaf._parent



