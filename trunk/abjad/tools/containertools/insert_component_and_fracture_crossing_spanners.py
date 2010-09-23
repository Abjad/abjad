from abjad.components._Component import _Component
from abjad.components.Container import Container


def insert_component_and_fracture_crossing_spanners(container, i, component):
   r'''Insert `component` into `container` at index `i`
   and fracture spanners::

      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> containertools.insert_component_and_fracture_crossing_spanners(staff, 1, Rest((1, 8)))
      [(spannertools.BeamSpanner(c'8, d'8, e'8, f'8), spannertools.BeamSpanner(c'8), spannertools.BeamSpanner(d'8, e'8, f'8)), 
       (spannertools.BeamSpanner(c'8), spannertools.BeamSpanner(c'8), spannertools.BeamSpanner( )), 
       (spannertools.BeamSpanner(d'8, e'8, f'8), spannertools.BeamSpanner( ), spannertools.BeamSpanner(d'8, e'8, f'8))]

   ::

      abjad> f(staff)
      \new Staff {
         c'8 [ ]
         r8
         d'8 [
         e'8
         f'8 ]
      }

   Return list of fractured spanners.

   .. versionchanged:: 1.1.2
      renamed ``containertools.insert_and_fracture( )`` to
      ``containertools.insert_component_and_fracture_crossing_spanners( )``.
   '''
   from abjad.tools import spannertools

   if not isinstance(container, Container):
      raise TypeError('must be container: %s' % container)

   assert isinstance(i, int)
   assert isinstance(component, _Component)

   result = [ ]
   component._parentage._switch(container)
   container._music.insert(i, component)
   if component.prev:
      #result.extend(component.prev.spanners.fracture(direction = 'right'))
      result.extend(spannertools.fracture_all_spanners_attached_to_component(
         component.prev, direction = 'right'))
   if component.next:
      #result.extend(component.next.spanners.fracture(direction = 'left')) 
      result.extend(spannertools.fracture_all_spanners_attached_to_component(
         component.next, direction = 'left'))

   return result
