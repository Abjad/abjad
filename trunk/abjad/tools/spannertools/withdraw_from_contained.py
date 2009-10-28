from abjad.component.component import _Component
from abjad.tools import check
from abjad.tools import iterate


def _withdraw_from_contained(components):
   '''Find every spanner contained in 'components'.
      Withdraw all components in 'components' from spanners.
      Return 'components'.
      The operation may leave discontiguous spanners.'''

   ## check components
   check.assert_components(components, contiguity = 'thread')

   ## withdraw from contained spanners
   for component in iterate.naive_forward(components, _Component):
      component.spanners._detach( )

   ## return components
   return components
