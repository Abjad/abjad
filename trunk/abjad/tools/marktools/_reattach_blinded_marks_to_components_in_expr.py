def _reattach_blinded_marks_to_components_in_expr(expr):
    '''Component copy operations can blind marks.
    Use this function to reattach blinded marks immediately after component copy operations.
    No other operations should blind marks.
    So do not use this function to repair incomplete implementation of other operations.
    Maybe can eliminated with targeted copy implementations.
    '''
    from abjad.tools import componenttools

    for component in componenttools.iterate_components_forward_in_expr(expr):
        for mark in component._marks_for_which_component_functions_as_start_component:
            mark._start_component = component
            #mark._bind_effective_context(mark.target_context)
            component._mark_entire_score_tree_for_later_update('marks')
