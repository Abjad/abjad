from abjad import *


def test_leaf_slip_01( ):
   '''Slip leaf from parentage and spanners.'''

   t = Voice(scale(4))
   Beam(t[:])
   Glissando(t[:])
  
   note = t[1]
   receipt = note.slip( )

   r'''\new Voice {
      c'8 [ \glissando
      e'8 \glissando
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [ \\glissando\n\te'8 \\glissando\n\tf'8 ]\n}"
