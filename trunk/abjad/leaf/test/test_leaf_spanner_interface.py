from abjad import *


### TODO - add many more tests ###


def test_leaf_spanner_interface_01( ):
   '''t.spanners.die( ) kills all spanners attaching to leaf t.'''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t[ : ])
   assert len(t[0].spanners.spanners) == 1
   t[0].spanners.die( )
   assert len(t[0].spanners.spanners) == 0


#### FUSE ###
#
#def test_leaf_spanner_interface_10( ):
#   '''t.spanners.fuse( ) fuses spanners to the left and to the right.'''
#   t = Staff(Note(0, (1, 8)) * 6)
#   Beam(t[0:2])
#   Beam(t[2:4])
#   Beam(t[4:6])
#   assert len(t.spanners.spanners) == 0
#   t[3].spanners.fuse( )
#   spanner = t[0].beam.spanner
#   for leaf in t:
#      assert leaf.beam.spanner is spanner
#      assert len(leaf.spanners.spanners) == 1
