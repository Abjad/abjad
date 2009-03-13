from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_spannable_components import _are_spannable_components


def components_fracture_around(spannable_components):
   '''Fracture all spanners to the left of the leftmost component in list.
      Fracture all spanners to the right of the rightmost component in list.
      Return spannable_components.
      
      Components in list must be successive.
      After fracturing around, some spanners maybe have been copied.'''

   if not _are_spannable_components(spannable_components):
      raise ContiguityError('input must be spannable components.')

   if len(spannable_components) > 0:

      leftmost_component = spannable_components[0]
      leftmost_component.spanners.fracture(direction = 'left')

      rightmost_component = spannable_components[-1]
      rightmost_component.spanners.fracture(direction = 'right')

   return spannable_components
