from abjad import *


def test_total_01( ):
   '''
   leaf.spanners knows about any spanners that span leaf directly.
   '''

   t = Voice(run(4))
   appictate(t)
   p = Beam(t[ : ])
   
   for leaf in t:
      total = leaf.spanners.total( )
      assert len(total) == 1
      assert total[0] is p


def test_total_02( ):
   '''
   leaf.spanners knows about any spanners that span the container
   which contains leaf.
   '''

   t = Voice(run(4))
   appictate(t)
   p = Beam(t)
   
   for leaf in t:
      total = leaf.spanners.total( )
      assert len(total) == 1
      assert total[0] is p


def test_total_03( ):
   '''
   leaf.spanners knows about spanners high up in the total of leaf.
   '''

   t = Voice(run(4))
   t.insert(2, Sequential(run(2)))
   appictate(t)
   p = Beam(t)

   r'''
   \new Voice {
      c'8
      cs'8
      {
         d'8
         ef'8
      }
      e'8
      f'8
   }
   '''

   for leaf in t.leaves:
      total = leaf.spanners.total( )
      assert len(total) == 1
      assert total[0] is p
