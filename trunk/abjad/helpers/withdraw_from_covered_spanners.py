from abjad.helpers.assert_components import assert_components
from abjad.tools import spannertools


def withdraw_from_covered_spanners(components):
   '''Find every spanner covered by 'components'.
      Withdraw all components in 'components' from covered spanners.
      Return 'components'.
      The operation always leaves all score trees in tact.'''

   ## check components
   assert_components(components, contiguity = 'thread')

   ## withdraw from covered spanners
   for spanner in spannertools.get_covered(components):
      spanner.clear( )

   ## return components
   return components
