def _get_dynamic_mark_format_contributions(component):
   '''.. versionadded:: 1.1.2
   '''
   from abjad.tools import contexttools

   result = [ ]
   dynamic_marks = contexttools.get_dynamic_marks_attached_to_start_component(component)
   for dynamic_mark in dynamic_marks:
      result.append(dynamic_mark.format)
   result.sort( )
   return result
