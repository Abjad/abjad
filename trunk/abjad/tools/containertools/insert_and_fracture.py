from abjad.component.component import _Component
from abjad.container import Container


def insert_and_fracture(container, i, component):
   r'''Insert component into container at index i.
      Fracture spanners to the left of index i.
      Fracture spanners to the right of index i.
      Return Python list of fractured spanners.

      For nonfracturing insert, use ``Container.__setitem__``.

      Example::

         abjad> t = Voice(construct.scale(4))
         abjad> Beam(t[:])
         abjad> containertools.insert_and_fracture(t, 1, Rest((1, 4)))
         abjad> print t.format

         \new Voice {
                 c'8 [ ]
                 r4
                 d'8 [
                 e'8
                 f'8 ]
         }'''

   assert isinstance(container, Container)
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
