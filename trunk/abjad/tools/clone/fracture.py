from abjad.component.component import _Component
from abjad.helpers.assert_components import assert_components
from abjad.tools import iterate
from abjad.tools.parenttools.ignore import _ignore
from abjad.tools.parenttools.restore import _restore
from abjad.tools import spannertools
import copy


def fracture(components, n = 1):
   '''Deep copy components in 'components'.
      Deep copy spanners that attach to any component in 'components'.
      Fracture spanners that attach to components not in 'components'.
      Return Python list of copied components.'''

   if n < 1:
      return [ ]

   assert_components(components, contiguity = 'thread')

   selection_components = set(iterate.naive(components, _Component))

   spanners = spannertools.get_crossing(components) 

   spanner_map = set([ ])
   for spanner in spanners:
      spanner_map.add((spanner, tuple(spanner[:])))
      for component in spanner[:]:
         if component not in selection_components:
            spanner._removeComponent(component)

   receipt = _ignore(components)
   
   result = copy.deepcopy(components)

   for component in result:
      component._update._markForUpdateToRoot( )

   _restore(receipt)

   for spanner, contents in spanner_map:
      spanner.clear( )
      spanner.extend(list(contents))

   for i in range(n - 1):
      result += fracture(components)

   return result
