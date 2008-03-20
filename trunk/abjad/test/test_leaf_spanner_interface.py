from abjad import *


### TODO - add many more tests ###


def test_leaf_spanner_interface_01( ):
   '''t.spanners.die( ) kills all spanners attaching to leaf t.'''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   assert len(t[0].spanners) == 1
   t[0].spanners.die( )
   assert len(t[0].spanners) == 0
