from abjad.tools.marktools.Comment import Comment


def get_comment_marks_attached_to_component(component):
   r'''.. versionadded:: 1.1.2

   Get comment marks attached to `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> marktools.Comment('comment 1')(staff[0])
      abjad> marktools.Comment('comment 2')(staff[0])
      abjad> f(staff)
      \new Staff {
         %% comment 1
         %% comment 2
         c'8 (
         d'8
         e'8
         f'8 )
      }
      
   ::
      
      abjad> marktools.get_comment_marks_attached_to_component(staff[0]) 
      (Comment('comment 1')(c'8), Comment('comment 2')(c'8))

   Return tuple of zero or more marks.
   '''

   result = [ ]
   for mark in component._marks_for_which_component_functions_as_start_component:
      if isinstance(mark, Comment):
         result.append(mark)

   result = tuple(result)
   return result
