def _withdraw_component_from_attached_spanners(component):
   '''Withdraw `component` from all attached spanners.
   '''

   ## externalization of (old) component spanner aggregator _detach( ) method
   for spanner in list(component.spanners._spanners):
      index = spanner.index(component)
      spanner._remove(component)
