from abjad import *


def test_BeamSpanner_fuse_01( ):
   '''Fuse works by reference to the right.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   left = BeamSpanner(t[ : 2])
   right = BeamSpanner(t[2 : 4])

   assert len(t.spanners.contained)
   assert left[ : ] == t[ : 2]
   assert left.components == tuple(t[ : 2])
   assert right[ : ] == t[2 : 4]
   assert right.components == tuple(t[2 : 4])

   left.fuse(right)
   spanners = t.spanners.contained

   assert len(spanners) == 1
