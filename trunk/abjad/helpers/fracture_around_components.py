from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_successive_components import _are_successive_components


def fracture_around_components(component_list):
   '''Fracture all spanners to the left of the leftmost component in list;
      fracture all spanners to the right of the rightmost component in list;
      return component list.
      
      Components in list must be successive.
      After fracturing around, some spanners maybe have been copied.'''

   ## TODO: a different check would be better here;
   ##       instead of _are_successive_components( )
   ##       it would be better to implement something generalized 
   ##       like _are_threadable_components.

   if not _are_successive_components(component_list):
      raise ContiguityError('component_list must be successive.')

   if len(component_list) > 0:

      leftmost_component = component_list[0]
      leftmost_component.spanners.fracture(direction = 'left')

      rightmost_component = component_list[-1]
      rightmost_component.spanners.fracture(direction = 'right')

   return component_list
