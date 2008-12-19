from abjad import *

def test_die_01( ):
   '''
   Aggregator die.
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])
   
   assert len(p.leaves) == len(p.components) == 4 
   assert len(t[0].spanners.mine) == len(t[0].spanners.total) == 1
   assert len(t[1].spanners.mine) == len(t[1].spanners.total) == 1
   assert len(t[2].spanners.mine) == len(t[2].spanners.total) == 1
   assert len(t[3].spanners.mine) == len(t[3].spanners.total) == 1
   assert check(t)
   
   t[0].spanners.die( )

   assert len(p.leaves) == len(p.components) == 0 
   assert len(t[0].spanners.mine) == len(t[0].spanners.total) == 0
   assert len(t[1].spanners.mine) == len(t[1].spanners.total) == 0
   assert len(t[2].spanners.mine) == len(t[2].spanners.total) == 0
   assert len(t[3].spanners.mine) == len(t[3].spanners.total) == 0
   assert check(t)
