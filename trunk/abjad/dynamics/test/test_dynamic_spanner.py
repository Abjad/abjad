from abjad import *


def test_dynamic_spanner_01( ):
   
   t = Voice(scale(4))
   Beam(t[:])
   Dynamic(t[:2], 'f')
   Dynamic(t[2:], 'p')

   r'''\new Voice {
      c'8 [ \f
      d'8
      e'8 \p
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [ \\f\n\td'8\n\te'8 \\p\n\tf'8 ]\n}"
   assert t[0].dynamics.effective == 'f'
   assert t[1].dynamics.effective == 'f'
   assert t[2].dynamics.effective == 'p'
   assert t[3].dynamics.effective == 'p'
