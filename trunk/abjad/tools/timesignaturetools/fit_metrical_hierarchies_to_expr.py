from abjad.tools import durationtools


def fit_metrical_hierarchies_to_expr(expr, metrical_hierarchies, starting_offset=None, depth=32):
    from abjad.tools import timesignaturetools

    offset_counter = durationtools.count_offsets_in_expr(expr)
    ordered_offsets = sorted(offset_counter, reverse=True)
    assert len(offset_count)

    if starting_offset is None:
        start_offset = durationtools.Offset(0)
    else:
        start_offset = durationtools.Offset(starting_offset)

    metrical_hierarchy_inventory = timesignaturetools.MetricalHierarchyInventory(metrical_hierarchies)
    longest_hierarchy = sorted(metrical_hierarchy_inventory, lambda x: x.duration)[0]
    longest_kernel_duration = max(x.duration for x in metrical_hierarchy_inventory)
    kernels = [x.generate_offset_kernel_to_depth(depth=depth) for x in metrical_hierarchy_inventory]
    
    current_start_offset = start_offset
    selected_hierarchies = []
    while current_start_offset < ordered_offsets[-1]:            
        # PROCEDURE:
        # pop offsets less than current_start_offset
        # then collect all offsets such that current_start_offset <= x <= current_stop_offset
        # if no offsets, make a best guess selection (how?) and continue to loop
        # otherwise, shift the collected offsets, taking current_start_offset as the origin
        # compare each kernel against the shifted offsets, caching the response as a pair
        # then sort the kernels by their responses, breaking ties somehow (fewest number of nodes?)
        # append the winner to selected_hierarchies
        # add the duration of the winner to current_start_offset
        # continue to loop
        while len(ordered_offsets) and ordered_offsets[-1] < start_offset:
            ordered_offsets.pop()
        current_stop_offset = current_start_offset + longest_kernel_duration
        current_offset_counter = {}
        for offset in reversed(ordered_offsets):
            if current_start_offset <= offset <= current_stop_offset:
                current_offset_counter[offset - current_start_offset] = offset_counter[offset]
            else:
                break
        if not current_offset_counter:
            winner = longest_hierarchy
        else: 
            # this is where we do the comparisons
            candidates = []
            for i, kernel in enumerate(kernels):
                response = kernel(current_offset_counter)
                candidates.append((response, i))
            candidates.sort(key=lambda x: x[0], reversed=True)
            winner = metrical_hierarchy_inventory[candidates[0]]
        selected_hierarchies.append(winner)
        current_start_offset += winner.duration 

    return selected_hierarchies
