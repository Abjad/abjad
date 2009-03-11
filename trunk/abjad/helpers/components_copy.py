from abjad.exceptions.exceptions import ContiguityError
from abjad.helpers.are_successive_components import _are_successive_components
from abjad.helpers.get_parent_and_index import _get_parent_and_index


## TODO: Finish implementation

def components_copy(successive_components):
   '''Deep copy components.
      Copy the portions of all spanners attaching to components.
      Leave components unchanged.
      Return Python list of deep copy of components.

      Example:'''

   # check input
   if not _are_successive_components(components):
      raise ContiguityError('input must be successive components.')

   for component in successive_components:

      parent, index = _get_parent_and_index(component) 
