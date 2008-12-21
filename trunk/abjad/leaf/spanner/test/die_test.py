from abjad import *


### TODO - rename die( ) to something less severe

def test_die_01( ):
   '''
   Call die( ) on the _LeafSpannerAggregator of any leaf.
   Spanners attaching directly to that leaf cut references
   to all constituent leaves.
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])
   
   assert len(p.leaves) == len(p.components) == 4 
   assert len(t[0].spanners.mine( )) == len(t[0].spanners.total( )) == 1
   assert len(t[1].spanners.mine( )) == len(t[1].spanners.total( )) == 1
   assert len(t[2].spanners.mine( )) == len(t[2].spanners.total( )) == 1
   assert len(t[3].spanners.mine( )) == len(t[3].spanners.total( )) == 1
   assert check(t)
   
   t[0].spanners.die( )

   assert len(p.leaves) == len(p.components) == 0 
   assert len(t[0].spanners.mine( )) == len(t[0].spanners.total( )) == 0
   assert len(t[1].spanners.mine( )) == len(t[1].spanners.total( )) == 0
   assert len(t[2].spanners.mine( )) == len(t[2].spanners.total( )) == 0
   assert len(t[3].spanners.mine( )) == len(t[3].spanners.total( )) == 0
   assert check(t)


def test_die_02( ):
   '''
   Calling die( ) on the _LeafSpannerAggregator of any leaf
   leaves spanners attaching to containers in the parentage 
   of leaf in tact.
   '''

   t = Voice(scale(4))
   p = Spanner(t)

   assert len(p.components) == 1
   assert len(p.leaves) == 4
   assert len(t[0].spanners.above( )) == 1 and len(t[0].spanners.mine( )) == 0
   assert len(t[1].spanners.above( )) == 1 and len(t[1].spanners.mine( )) == 0
   assert len(t[2].spanners.above( )) == 1 and len(t[2].spanners.mine( )) == 0
   assert len(t[3].spanners.above( )) == 1 and len(t[3].spanners.mine( )) == 0
   assert check(t)

   t[0].spanners.die( )

   assert len(p.components) == 1
   assert len(p.leaves) == 4
   assert len(t[0].spanners.above( )) == 1 and len(t[0].spanners.mine( )) == 0
   assert len(t[1].spanners.above( )) == 1 and len(t[1].spanners.mine( )) == 0
   assert len(t[2].spanners.above( )) == 1 and len(t[2].spanners.mine( )) == 0
   assert len(t[3].spanners.above( )) == 1 and len(t[3].spanners.mine( )) == 0
   assert check(t)


def test_die_03( ):
   '''
   Calling die( ) on a _LeafSpannerAggregator releases
   multiple spanners attaching to leaf.
   '''

   t = Voice(scale(4))
   p1 = Spanner(t[ : ])
   p2 = Spanner(t[ : ])
   p3 = Spanner(t[ : ])

   assert len(p1.components) == len(p2.components) == len(p3.components) == 4
   assert len(p1.leaves) == len(p2.leaves) == len(p3.leaves) == 4
   assert len(t[0].spanners.above( )) == 0 and len(t[0].spanners.mine( )) == 3
   assert len(t[1].spanners.above( )) == 0 and len(t[1].spanners.mine( )) == 3
   assert len(t[2].spanners.above( )) == 0 and len(t[2].spanners.mine( )) == 3
   assert len(t[3].spanners.above( )) == 0 and len(t[3].spanners.mine( )) == 3
   assert check(t)

   t[0].spanners.die( )

   assert len(p1.components) == len(p2.components) == len(p3.components) == 0
   assert len(p1.leaves) == len(p2.leaves) == len(p3.leaves) == 0
   assert len(t[0].spanners.above( )) == 0 and len(t[0].spanners.mine( )) == 0
   assert len(t[1].spanners.above( )) == 0 and len(t[1].spanners.mine( )) == 0
   assert len(t[2].spanners.above( )) == 0 and len(t[2].spanners.mine( )) == 0
   assert len(t[3].spanners.above( )) == 0 and len(t[3].spanners.mine( )) == 0
   assert check(t)


def test_die_04( ):
   '''
   You can call die(**kwargs) on any _LeafSpannerAggregator
   to cause only certain spanners attaching to leaf to retract.
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])
   b = Beam(t[ : ])

   assert len(p.components) == len(b.components) == 4
   assert len(p.leaves) == len(b.leaves) == 4
   assert len(t[0].spanners.above( )) == 0 and len(t[0].spanners.mine( )) == 2
   assert len(t[1].spanners.above( )) == 0 and len(t[1].spanners.mine( )) == 2
   assert len(t[2].spanners.above( )) == 0 and len(t[2].spanners.mine( )) == 2
   assert len(t[3].spanners.above( )) == 0 and len(t[3].spanners.mine( )) == 2
   assert check(t)

   t[0].spanners.die(classname = 'Beam')

   assert len(p.components) == len(p.leaves) == 4
   assert len(b.components) == len(b.leaves) == 0
   assert len(t[0].spanners.above( )) == 0 and len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.above( )) == 0 and len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.above( )) == 0 and len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.above( )) == 0 and len(t[3].spanners.mine( )) == 1
   assert check(t)
