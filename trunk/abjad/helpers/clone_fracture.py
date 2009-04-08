from abjad.component.component import _Component
from abjad.helpers.assert_components import assert_components
from abjad.helpers.ignore_parent import \
   _ignore_parent
from abjad.helpers.get_crossing_spanners import get_crossing_spanners
from abjad.helpers.iterate import iterate
from abjad.helpers.restore_outgoing_reference_to_parent import \
   restore_outgoing_reference_to_parent
import copy


def clone_fracture(components, n = 1):
   '''Deep copy components in 'components'.
      Deep copy spanners that attach to any component in 'components'.
      Fracture spanners that attach to components not in 'components'.
      Return Python list of copied components.'''

   if n < 1:
      return [ ]

   assert_components(components, contiguity = 'thread')

   selection_components = set(iterate(components, _Component))

   spanners = get_crossing_spanners(components) 

   spanner_map = set([ ])
   for spanner in spanners:
      spanner_map.add((spanner, tuple(spanner[:])))
      for component in spanner[:]:
         if component not in selection_components:
            spanner._removeComponent(component)

   receipt = _ignore_parent(components)
   
   result = copy.deepcopy(components)

   for component in result:
      component._update._markForUpdateToRoot( )

   restore_outgoing_reference_to_parent(receipt)

   for spanner, contents in spanner_map:
      spanner.clear( )
      spanner.extend(list(contents))

   for i in range(n - 1):
      result += clone_fracture(components)

   return result
