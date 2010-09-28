from abjad.components._Context import _Context


def get_all_context_marks_attached_to_any_improper_parent_of_component(component):


   '''.. versionadded:: 1.1.2

   Get all context marks attached to any improper parent of `component`.

   Return unordered set of zero or more context marks.
   '''
   from abjad.tools import componenttools

   result = set([ ])

   for component in componenttools.get_improper_parentage_of_component(component):
      for mark in component.marks:
         if mark.target_context is not None:
            if issubclass(mark.target_context, _Context):
               result.add(mark)

   return result
