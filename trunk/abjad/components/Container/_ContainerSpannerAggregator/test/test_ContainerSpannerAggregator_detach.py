from abjad import *


def test_ContainerSpannerAggregator_detach_01( ):
   '''t.spanners._detach( ) detaches all spanners attaching to container t.'''

   t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   p1 = BeamSpanner(t[:])
   p2 = GlissandoSpanner(t[:])

   r'''
   \new Staff {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 ]
      }
   }
   '''

   t[0].spanners._detach( )

   r'''
   \new Staff {
      {
         c'8
         d'8
      }
      {
         e'8 [ \glissando
         f'8 ]
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8 [ \\glissando\n\t\tf'8 ]\n\t}\n}"
