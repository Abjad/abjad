from abjad.component.component import _Component
from abjad.helpers.assert_components import assert_components
from abjad.tools import iterate


def _withdraw_from_contained_spanners(components):
   '''Find every spanner contained in 'components'.
      Withdraw all components in 'components' from spanners.
      Return 'components'.
      The operation may leave discontiguous spanners.'''

   ## check components
   assert_components(components, contiguity = 'thread')

   ## withdraw from contained spanners
   for component in iterate.naive(components, _Component):
      component.spanners._detach( )

   ## return components
   return components
