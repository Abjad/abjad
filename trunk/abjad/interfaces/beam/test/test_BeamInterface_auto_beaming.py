from abjad import *


def test_beam_interface_auto_beaming_01( ):
   '''Interface to LilyPond autoBeaming context setting.
   Set to true or false.'''

   t = Staff(macros.scale(4))
   t.beam.auto_beaming = True

   r'''
   \new Staff \with {
           autoBeaming = ##t
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff \\with {\n\tautoBeaming = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_beam_interface_auto_beaming_02( ):
   '''Clear with none.'''

   t = Staff(macros.scale(4))
   t.beam.auto_beaming = True
   t.beam.auto_beaming = None

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
