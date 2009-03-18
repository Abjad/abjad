from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_strictly_contiguous_components_in_same_score import _are_strictly_contiguous_components_in_same_score
from abjad.helpers.get_parent_and_index import _get_parent_and_index


## TODO: Finish implementation

def components_copy(components):
   '''Deep copy components.
      Copy the portions of all spanners attaching to components.
      Leave components unchanged.
      Return Python list of deep copy of components.

      Example:'''

   # check input
   if not _are_strictly_contiguous_components_in_same_score(components):
      raise ContiguityError(
         'Input must be strictly contiguous components in same score.')

   for component in components:

      parent, index = _get_parent_and_index(component) 
