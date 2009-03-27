from abjad.helpers.assert_components import assert_components
from abjad.helpers.get_parent_and_indices import get_parent_and_indices


## TODO: Finish implementation

def components_copy(components):
   '''Deep copy components.
      Copy the portions of all spanners attaching to components.
      Leave components unchanged.
      Return Python list of deep copy of components.

      Example:'''

   # check input
   assert_components(components, contiguity = 'strict', share = 'score')

   for component in components:

      parent, start, stop = get_parent_and_indices(component) 
