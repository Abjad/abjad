from abjad.component import _Component
from abjad.container import Container


def insert_component_and_fracture_crossing_spanners(container, i, component):
   r'''Insert `component` into `container` at index `i`
   and fracture spanners::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> Beam(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> containertools.insert_component_and_fracture_crossing_spanners(staff, 1, Rest((1, 8)))
      [(Beam(c'8, d'8, e'8, f'8), Beam(c'8), Beam(d'8, e'8, f'8)), 
       (Beam(c'8), Beam(c'8), Beam( )), 
       (Beam(d'8, e'8, f'8), Beam( ), Beam(d'8, e'8, f'8))]

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

   if not isinstance(container, Container):
      raise TypeError('must be container: %s' % container)

   assert isinstance(i, int)
   assert isinstance(component, _Component)

   result = [ ]
   component.parentage._switch(container)
   container._music.insert(i, component)
   if component.prev:
      result.extend(component.prev.spanners.fracture(direction = 'right'))
   if component.next:
      result.extend(component.next.spanners.fracture(direction = 'left')) 

   return result
