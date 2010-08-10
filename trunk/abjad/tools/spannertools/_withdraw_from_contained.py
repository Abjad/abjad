from abjad.components._Component import _Component


def _withdraw_from_contained(components):
   '''Find every spanner contained in 'components'.
   Withdraw all components in 'components' from spanners.
   Return 'components'.
   The operation may leave discontiguous spanners.
   '''
   from abjad.tools import componenttools

   ## check components
   assert componenttools.all_are_thread_contiguous_components(components)

   ## withdraw from contained spanners
   for component in componenttools.iterate_components_forward_in_expr(components, _Component):
      component.spanners._detach( )

   ## return components
   return components
