from abjad.tools.contexttools.Mark import Mark


def detach_context_marks_attached_to_start_component(start_component, klasses = (Mark, )):
   r'''.. versionadded:: 1.1.2

   Detach context marks attached to `start_component`::

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

      abjad> contexttools.detach_context_marks_attached_to_start_component(staff[0])
      (DynamicMark('p'),)

   ::

      abjad> f(staff)
      \new Staff {
         \clef "treble"
         c'8
         d'8
         e'8
         f'8
      }
   Return tuple of zero or marks.
   '''

   marks = [ ]
   for mark in start_component._marks_for_which_component_functions_as_start_component[:]:
      if isinstance(mark, klasses):
         mark.detach_mark( )
         marks.append(mark)
   return tuple(marks)
