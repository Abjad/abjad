from abjad.tools.contexttools.DynamicMark import DynamicMark
from abjad.tools.contexttools.get_context_marks_attached_to_start_component import \
   get_context_marks_attached_to_start_component


def get_dynamic_marks_attached_to_start_component(start_component):
   r'''.. versionadded:: 1.1.2

   Get dynamic marks attached to `start_component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> clef_mark = contexttools.ClefMark('treble')(staff)
      abjad> dynamic_mark = contexttools.DynamicMark('p')(staff[0])
      abjad> f(staff)
      \new Staff {
         \clef "treble"
         c'8 \p
         d'8
         e'8
         f'8
      }
      
   ::
      
      abjad> contexttools.get_dynamic_marks_attached_to_start_component(staff[0]) 
      (DynamicMark('p')(c'8),)

   Return tuple of zero or more dynamic marks.
   '''

   return get_context_marks_attached_to_start_component(start_component, klasses = (DynamicMark, ))
