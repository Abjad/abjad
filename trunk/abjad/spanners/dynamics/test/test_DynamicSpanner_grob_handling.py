from abjad import *


def test_dynamic_spanner_grob_handling_01( ):

   t = Voice(macros.scale(4))
   Beam(t[:])
   p = Dynamic(t[:], 'f')
   p.thickness = 3

   r'''
   \new Voice {
      \override DynamicText #'thickness = #3
      c'8 [ \f
      d'8
      e'8
      f'8 ]
      \revert DynamicText #'thickness
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t\\override DynamicText #'thickness = #3\n\tc'8 [ \\f\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert DynamicText #'thickness\n}"
