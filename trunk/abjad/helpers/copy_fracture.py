from abjad.component.component import _Component
from abjad.helpers.assert_components import assert_components
from abjad.helpers.cut_outgoing_reference_to_parent import \
   _cut_outgoing_reference_to_parent
from abjad.helpers.get_crossing_spanners import get_crossing_spanners
from abjad.helpers.iterate import iterate
from abjad.helpers.restore_outgoing_reference_to_parent import \
   restore_outgoing_reference_to_parent
import copy


def copy_fracture(components):
   '''Deep copy components in 'components'.
      Deep copy spanners that attach to any component in 'components'.
      Fracture spanners that attach to components not in 'components'.
      Return Python list of copied components.'''

   assert_components(components, contiguity = 'thread')

   selection_components = set(iterate(components, _Component))

   spanners = get_crossing_spanners(components) 

   spanner_map = set([ ])
   for spanner in spanners:
      spanner_map.add((spanner, tuple(spanner[:])))
      for component in spanner[:]:
         if component not in selection_components:
            spanner._removeComponent(component)

   receipt = _cut_outgoing_reference_to_parent(components)
   
   result = copy.deepcopy(components)

   for component in result:
      component._update._markForUpdateToRoot( )

   restore_outgoing_reference_to_parent(receipt)

   for spanner, contents in spanner_map:
      spanner.clear( )
      spanner.extend(list(contents))

   return result
