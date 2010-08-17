from abjad import *


def test_LeafSpannerAggregator_detach_01( ):
   '''t.spanners._detach( ) detaches all spanners attached to leaf t.'''

   t = Staff(macros.scale(4))
   p1 = spannertools.BeamSpanner(t[ : ])
   p2 = spannertools.GlissandoSpanner(t[ : ])

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


def test_LeafSpannerAggregator_detach_02( ):
   '''t.spanners._detach( ) returns a SpannersReceipt.'''

   t = Staff(macros.scale(4))
   beam = spannertools.BeamSpanner(t[ : ])
   glissando = spannertools.GlissandoSpanner(t[ : ])

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
