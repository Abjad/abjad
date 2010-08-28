from abjad import *


def test_LilyPondContextSettingComponentPlugIn___setattr___01( ):

   t = Staff(macros.scale(4))
   t.set.font_size = -3

   r'''
   \new Staff \with {
           fontSize = #-3
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff \\with {\n\tfontSize = #-3\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
