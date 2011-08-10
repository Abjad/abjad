from abjad.tools.contexttools.ContextMark import ContextMark


def detach_all_context_marks_attached_to_component(start_component, klasses = (ContextMark, )):
   r'''.. versionadded:: 2.0

   Detach context marks attached to `start_component`::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
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

      abjad> contexttools.detach_all_context_marks_attached_to_component(staff[0])
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

   .. versionchanged:: 1.1.2
      renamed ``contexttools.detach_context_marks_attached_to_start_component( )`` to
      ``contexttools.detach_all_context_marks_attached_to_component( )``.
   '''

   marks = [ ]
   for mark in start_component._marks_for_which_component_functions_as_start_component[:]:
      if isinstance(mark, klasses):
         mark.detach_mark( )
         marks.append(mark)
   return tuple(marks)
