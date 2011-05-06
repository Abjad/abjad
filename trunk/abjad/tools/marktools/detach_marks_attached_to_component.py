from abjad.tools.marktools.get_marks_attached_to_component import get_marks_attached_to_component


def detach_marks_attached_to_component(component):
   r'''.. versionadded:: 1.1.2
   
   Detach marks attached to `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> marktools.Articulation('^')(staff[0])
      abjad> marktools.Comment('comment 1')(staff[0])
      abjad> marktools.LilyPondCommandMark('slurUp')(staff[0])

   ::

      abjad> f(staff)
      \new Staff {
         % comment 1
         \slurUp
         c'8 -\marcato (
         d'8
         e'8
         f'8 )
      }

   ::

      abjad> marktools.get_marks_attached_to_component(staff[0])
      (Articulation('^', '-')(c'8), Comment('comment 1')(c'8), LilyPondCommandMark('slurUp')(c'8))

   ::

      abjad> marktools.detach_marks_attached_to_component(staff[0])
      (Articulation('^', '-'), Comment('comment 1'), LilyPondCommandMark('slurUp'))

   ::

      abjad> marktools.get_marks_attached_to_components(staff[0])
      ()
      
   Return tuple or zero or more marks detached.
   '''

   marks = [ ]
   for mark in get_marks_attached_to_component(component):
      mark.detach_mark( )
      marks.append(mark)

   return tuple(marks)
