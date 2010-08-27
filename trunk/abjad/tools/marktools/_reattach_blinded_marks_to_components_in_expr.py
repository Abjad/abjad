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
      #print component, component.marks
      #for mark in component._marks_for_which_component_functions_as_mark_context:
      #   mark._target_context = component
      #   all_marks_in_expr.add(mark)
      for mark in component._marks_for_which_component_functions_as_start_component:
         #print mark, mark.start_component, mark.target_context, mark.effective_context
         mark._start_component = component
         mark._bind_effective_context(mark.target_context)
         #print mark, mark.start_component, mark.target_context, mark.effective_context
         all_marks_in_expr.add(mark)

   ## this suite should be completely unnecessary
   total_blinded_marks_in_expr_unable_to_reattach_to_start_component = 0
   for mark in all_marks_in_expr:
      if mark.start_component is None:
         mark.detach_mark( )
         total_blinded_marks_in_expr_unable_to_reattach_to_start_component += 1
   if total_blinded_marks_in_expr_unable_to_reattach_to_start_component:
      raise Exception('this is weird; mark should ALWAYS find a start component to reattach to.')

   return total_blinded_marks_in_expr_unable_to_reattach_to_start_component
