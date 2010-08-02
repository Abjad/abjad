from abjad import *


def test_leaf_spanner_aggregator_detach_01( ):
   '''t.spanners._detach( ) detaches all spanners attached to leaf t.'''

   t = Staff(macros.scale(4))
   p1 = Beam(t[ : ])
   p2 = Glissando(t[ : ])

   r'''
   \new Staff {
      c'8 [ \glissando
      d'8 \glissando
      e'8 \glissando
      f'8 ]
   }
   '''

   t[0].spanners._detach( )

   r'''
   \new Staff {
      c'8
      d'8 [ \glissando
      e'8 \glissando
      f'8 ]
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\td'8 [ \\glissando\n\te'8 \\glissando\n\tf'8 ]\n}"
   assert componenttools.is_well_formed_component(t)


def test_leaf_spanner_aggregator_detach_02( ):
   '''t.spanners._detach( ) returns a SpannersReceipt.'''

   t = Staff(macros.scale(4))
   beam = Beam(t[ : ])
   glissando = Glissando(t[ : ])

   r'''
   \new Staff {
      c'8 [ \glissando
      d'8 \glissando
      e'8 \glissando
      f'8 ]
   }
   '''

   receipt = t[0].spanners._detach( )

#   assert len(receipt._pairs) == 2
#   assert (beam, 0) in receipt._pairs
#   assert (glissando, 0) in receipt._pairs 
