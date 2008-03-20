from abjad import *


### TODO - add many more tests ###


def test_container_spanner_interface_01( ):
   '''t.spanners.die( ) kills all spanners attaching to container t.'''
   t = Staff(Note(0, (1, 8)) * 8)
   Beam(t)
   assert len(t.spanners) == 1
   t.spanners.die( )
   assert len(t.spanners) == 0
