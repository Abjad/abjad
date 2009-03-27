from abjad.helpers.assert_components import assert_components
from abjad.helpers.cut_outgoing_reference_to_parent import \
   _cut_outgoing_reference_to_parent
from abjad.helpers.get_crossing_spanners import get_crossing_spanners
from abjad.helpers.restore_outgoing_reference_to_parent import \
   restore_outgoing_reference_to_parent
import copy


def copy_covered(components):
   '''Withdraw components in 'components' from crossing spanners.
      Preserve spanners that 'components' cover.
      Deep copy components in 'components'.
      Reapply crossing spanners to 'components'.
      Return copy of 'components' with covered spanners.
      The 'components' must be thread-contiguous.'''

   assert_components(components, contiguity = 'thread')

   spanners = get_crossing_spanners(components) 
   for spanner in spanners:
      spanner._blockAllComponents( )

   receipt = _cut_outgoing_reference_to_parent(components)

   result = copy.deepcopy(components)

   restore_outgoing_reference_to_parent(receipt)

   for spanner in spanners:
      spanner._unblockAllComponents( )
      
   return result
