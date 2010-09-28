def get_all_marks_attached_to_component(component):
   '''.. versionadded:: 1.1.2

   Get all marks attached to `component`'::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> comment_mark = marktools.Comment('beginning of note content')(staff[0])
      abjad> marktools.LilyPondCommandMark('slurDotted')(staff[0])

   ::

      abjad> marktools.get_all_marks_attached_to_component(staff[0]) 
      (Comment('beginning of note content')(c'8), LilyPondCommandMark('slurDotted')(c'8))

   Return tuple of zero or more marks.
   '''

   marks = component._marks_for_which_component_functions_as_start_component
   marks = tuple(marks)

   return marks
