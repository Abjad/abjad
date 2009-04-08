from abjad.helpers.assert_components import assert_components
from abjad.helpers.ignore_parent import \
   _ignore_parent
from abjad.helpers.get_crossing_spanners import get_crossing_spanners
from abjad.helpers.restore_outgoing_reference_to_parent import \
   restore_outgoing_reference_to_parent
import copy


def clone_covered(components, n = 1):
   '''Withdraw components in 'components' from crossing spanners.
      Preserve spanners that 'components' cover.
      Deep copy components in 'components'.
      Reapply crossing spanners to 'components'.
      Return copy of 'components' with covered spanners.
      The 'components' must be thread-contiguous.'''
   
   if n < 1:
      return [ ]

   assert_components(components, contiguity = 'thread')

   spanners = get_crossing_spanners(components) 
   for spanner in spanners:
      spanner._blockAllComponents( )

   receipt = _ignore_parent(components)

   result = copy.deepcopy(components)
   for component in result:
      component._update._markForUpdateToRoot( )

   restore_outgoing_reference_to_parent(receipt)

   for spanner in spanners:
      spanner._unblockAllComponents( )

   for i in range(n - 1):
      result += clone_covered(components)
      
   return result
