from abjad import *


def test_contexttools_get_context_marks_attached_to_start_component_01( ):

   staff = Staff(macros.scale(4))
   clef_mark = contexttools.ClefMark('treble')(staff)
   dynamic_mark = contexttools.DynamicMark('p')(staff[0])

   r'''
   \new Staff {
      \clef "treble"
      c'8 \p
      d'8
      e'8
      f'8
   }
   '''

   context_marks = contexttools.get_context_marks_attached_to_start_component(staff[0]) 

   assert dynamic_mark in context_marks
   assert len(context_marks) == 1
