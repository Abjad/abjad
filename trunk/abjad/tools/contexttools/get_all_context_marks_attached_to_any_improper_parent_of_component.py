from abjad.components._Context import _Context


def get_all_context_marks_attached_to_any_improper_parent_of_component(component):


   r'''.. versionadded:: 1.1.2

   Get all context marks attached to any improper parent of `component`::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.ClefMark('treble')(staff)
      ClefMark('treble')(Staff{4})
      abjad> contexttools.DynamicMark('f')(staff[0])
      DynamicMark('f')(c'8)

   ::

      abjad> f(staff)
      \new Staff {
         \clef "treble"
         c'8 \f
         d'8
         e'8
         f'8
      }

   ::

      abjad> contexttools.get_all_context_marks_attached_to_any_improper_parent_of_component(staff[0])
      set([DynamicMark('f')(c'8), ClefMark('treble')(Staff{4})])

   Return unordered set of zero or more context marks.
   '''
   from abjad.tools import componenttools

   result = set([ ])

   for component in componenttools.get_improper_parentage_of_component(component):
      for mark in component.marks:
         #if mark.target_context is not None:
         if getattr(mark, 'target_context', None) is not None:
            if issubclass(mark.target_context, _Context):
               result.add(mark)

   return result
