from abjad.tools import check
from abjad.tools import parenttools


def slip(components):
   '''Iterate components.
      Give spanners attached directly to container to children.
      Give children to parent.
      Return component.'''

   check.assert_components(components)
   for component in components:
      parent, start, stop = parenttools.get_with_indices([component])
      result = parent[start:stop+1] = list(component.music)
   return components
