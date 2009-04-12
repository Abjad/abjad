from abjad import *


def test_leaf_spanner_aggregator_reattach_01( ):
   '''Reattach with receipt.'''

   t = Staff(scale(4))
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

   receipt = t[0].spanners._detach( )

   r'''
   \new Staff {
      c'8
      d'8 [ \glissando
      e'8 \glissando
      f'8 ]
   }
   '''

   t[0].spanners._reattach(receipt)

   r'''
   \new Staff {
      c'8 [ \glissando
      d'8 \glissando
      e'8 \glissando
      f'8 ]
   }
   '''
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 [ \\glissando\n\td'8 \\glissando\n\te'8 \\glissando\n\tf'8 ]\n}"
