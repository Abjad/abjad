from abjad import *


def test_tuplet_bracket_interface_tuplet_full_length_01( ):

   t = Staff([ ])
   t.tuplet_bracket.tuplet_full_length = True

   r'''
   \new Staff \with {
           tupletFullLength = ##t
   } {
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff \\with {\n\ttupletFullLength = ##t\n} {\n}'

   t.tuplet_bracket.tuplet_full_length = False

   r'''
   \new Staff \with {
           tupletFullLength = ##f
   } {
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff \\with {\n\ttupletFullLength = ##f\n} {\n}'

   t.tuplet_bracket.tuplet_full_length = None

   r'''
   \new Staff {
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Staff {\n}'
