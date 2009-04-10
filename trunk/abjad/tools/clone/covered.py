from abjad.helpers.assert_components import assert_components
from abjad.tools.parenttools.ignore import _ignore
from abjad.tools.parenttools.restore import _restore
from abjad.tools import spannertools
import copy


def covered(components, n = 1):
   '''Withdraw components in 'components' from crossing spanners.
      Preserve spanners that 'components' cover.
      Deep copy components in 'components'.
      Reapply crossing spanners to 'components'.
      Return copy of 'components' with covered spanners.
      The 'components' must be thread-contiguous.'''
   
   if n < 1:
      return [ ]

   assert_components(components, contiguity = 'thread')

   spanners = spannertools.get_crossing(components) 
   for spanner in spanners:
      spanner._blockAllComponents( )

   receipt = _ignore(components)

   result = copy.deepcopy(components)
   for component in result:
      component._update._markForUpdateToRoot( )

   _restore(receipt)

   for spanner in spanners:
      spanner._unblockAllComponents( )

   for i in range(n - 1):
      result += covered(components)
      
   return result
