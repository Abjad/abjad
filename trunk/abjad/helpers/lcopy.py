from abjad.containers.container import Container
from abjad.leaf.leaf import _Leaf

def lcopy(expr, start = 0, stop = None):
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

   if isinstance(expr, _Leaf):
      return expr.copy( )

   leaves = expr.leaves
   assert start <= len(leaves)
   assert stop > start or stop is None

   governor = leaves[start]._parentage._governor
   governor_copy = governor.copy( )

   ### TODO -- implement Measure.trim( )

   return None
