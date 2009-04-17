from abjad.tools import check


def fracture_crossing(components):
   r'''Fracture to the left of the leftmost component.
   Fracture to the right of the rightmost component.
   Do not fracture spanners of any components at higher levels of score.
   Do not fracture spanners of any components at lower levels of score.
   Return components.
   
   Components must be thread-contiguous.
   Some spanners may copy during fracture.
   This helper is public-safe.

   Example::

      t = Staff(Container(construct.run(2)) * 3)
      pitchtools.diatonicize(t)
      Crescendo(t)
      Beam(t[:])
      Trill(t.leaves)

      \new Staff {
         {
            c'8 [ \< \startTrillSpan
            d'8
         }
         {
            e'8
            f'8
         }
         {
            g'8
            a'8 ] \! \stopTrillSpan
         }   }

      spannertools.fracture_crossing(t[1:2])

      \new Staff {
         {
            c'8 [ \< \startTrillSpan
            d'8 ]
         }
         {
            e'8 [
            f'8 ]
         }
         {
            g'8 [
            a'8 ] \! \stopTrillSpan
         }
      }'''

   check.assert_components(components, contiguity = 'thread')

   if len(components) > 0:

      leftmost_component = components[0]
      leftmost_component.spanners.fracture(direction = 'left')

      rightmost_component = components[-1]
      rightmost_component.spanners.fracture(direction = 'right')

   return components
