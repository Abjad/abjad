def _reattach_blinded_marks_to_components_in_expr(expr):
   '''Component copy operations can blind marks.
   Use this function to reattach blinded marks immediately after component copy operations.
   No other operations should blind marks.
   So do not use this function to repair incomplete implementation of other operations.
   '''
   from abjad.tools import componenttools

   #print 'reattaching blinded marks ...'
   all_marks_in_expr = set([ ])
   for component in componenttools.iterate_components_forward_in_expr(expr):
      for mark in component._marks_for_which_component_functions_as_mark_context:
         mark._context = component
         all_marks_in_expr.add(mark)
      for mark in component._marks_for_which_component_functions_as_start_component:
         mark._start_component = component
         all_marks_in_expr.add(mark)

   total_blinded_marks_in_expr_unable_to_reattach_to_both_context_and_start_component = 0
   for mark in all_marks_in_expr:
      if bool(mark.context is None) != bool(mark.start_component is None):
         mark.detach_mark_from_context_and_start_component( )
         total_blinded_marks_in_expr_unable_to_reattach_to_both_context_and_start_component += 1

   return total_blinded_marks_in_expr_unable_to_reattach_to_both_context_and_start_component
