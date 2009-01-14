from abjad import *


def test_container_spanner_aggregator_detach_01( ):
   '''
   t.spanners.detach( ) detaches all spanners attaching to container t.
   '''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   p1 = Beam(t[ : ])
   p2 = Glissando(t[ : ])

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

   t[0].spanners.detach( )

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

   assert t.format == "\\new Staff {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8 [ \\glissando\n\t\tf'8 ]\n\t}\n}"
   assert check(t)
