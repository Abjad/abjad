def get_all_comment_marks_attached_to_component(component):
   '''.. versionadded:: 1.1.2

   Get all comment marks attached to component.
   '''
   from abjad.tools import marktools

   result = set([ ])
   for mark in component.marks:
      if isinstance(mark, marktools.CommentMark):
         result.add(mark)
   return result
