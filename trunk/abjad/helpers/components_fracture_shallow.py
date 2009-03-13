from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_spannable_components import _are_spannable_components


def components_fracture_shallow(spannable_components):
   r'''Fracture to the left of the leftmost component.
      Fracture to the right of the rightmost component.
      Do not fracture spanners of any components at higher levels of score.
      Do not fracture spanners of any components at lower levels of score.
      Return spannable_components.
      
      Components in list must be successive.
      Some spanners may copy during fracture.
      This helper is public-safe.

      Example:

      t = Staff(Sequential(run(2)) * 3)
      diatonicize(t)
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

      components_fracture_shallow(t[1:2])

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

   if not _are_spannable_components(spannable_components):
      raise ContiguityError('input must be spannable components.')

   if len(spannable_components) > 0:

      leftmost_component = spannable_components[0]
      leftmost_component.spanners.fracture(direction = 'left')

      rightmost_component = spannable_components[-1]
      rightmost_component.spanners.fracture(direction = 'right')

   return spannable_components
