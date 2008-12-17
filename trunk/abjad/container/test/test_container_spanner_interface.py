from abjad import *


### TODO - add many more tests ###


def test_spanners_01( ):
   '''
   t.spanners.die( ) kills all spanners attaching to leaves in container t.
   '''

   t = Staff(run(8))
   appictate(t)
   Beam(t)
   assert len(t.spanners) == 1
   t.spanners.die( )
   assert len(t.spanners) == 0



