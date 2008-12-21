from abjad import *


### TODO - add many more tests ###


def test_leaf_spanner_interface_01( ):
   '''t.spanners.die( ) kills all spanners attaching to leaf t.'''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t[ : ])
   #assert len(t[0].spanners) == 1
   assert len(t[0].spanners.mine( )) == 1
   t[0].spanners.die( )
   #assert len(t[0].spanners) == 0
   assert len(t[0].spanners.mine( )) == 0


### FUSE ###

def test_leaf_spanner_interface_10( ):
   '''t.spanners.fuse( ) fuses spanners to the left and to the right.'''
   t = Staff(Note(0, (1, 8)) * 6)
   Beam(t[0:2])
   Beam(t[2:4])
   Beam(t[4:6])
   #assert len(t.spanners) == 3
   assert len(t.spanners.get( )) == 3
   t[3].spanners.fuse( )
   #assert len(t.spanners) == 1
   assert len(t.spanners.get( )) == 1
   spanner = t[0].beam.spanner
   for n in t:
      assert n.beam.spanner is spanner
      #assert len(n.spanners) == 1
      assert len(n.spanners.mine( )) == 1
