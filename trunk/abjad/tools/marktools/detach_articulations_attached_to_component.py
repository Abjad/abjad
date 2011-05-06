from abjad.tools.marktools.get_articulations_attached_to_component import get_articulations_attached_to_component


def detach_articulations_attached_to_component(component):
   r'''.. versionadded:: 1.1.2
   
   Detach articulations attached to `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> marktools.Articulation('^')(staff[0])
      abjad> marktools.Articulation('.')(staff[0])

   ::

      abjad> f(staff)
      \new Staff {
         c'8 -\marcato -\staccato (
         d'8
         e'8
         f'8 )
      }

   ::

      abjad> marktools.get_articulations_attached_to_component(staff[0])
      (Articulation('^', '-')(c'8), Articulation('.', '-')(c'8))

   ::

      abjad> marktools.detach_articulations_attached_to_component(staff[0])
      (Articulation('^', '-'), Articulation('.', '-'))

   ::

      abjad> marktools.get_articulations_attached_to_components(staff[0])
      ()
      
   Return tuple or zero or more articulations detached.
   '''

   articulations = [ ]
   for articulation in get_articulations_attached_to_component(component):
      articulation.detach_mark( )
      articulations.append(articulation)

   return tuple(articulations)
