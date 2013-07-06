import copy


def copy_components_and_covered_spanners(components, n=1):
    r'''.. versionadded:: 1.1

    Copy `components` and covered spanners.

    The `components` must be thread-contiguous.

    Covered spanners are those spanners that cover `components`.

    The steps taken in this function are as follows.
    Withdraw `components` from crossing spanners.
    Preserve spanners that `components` cover.
    Deep copy `components`.
    Reapply crossing spanners to source `components`.
    Return copied components with covered spanners.

    ::

        >>> staff = Staff(r"abj: | 2/8 c'8 ( d'8 || 2/8 e'8 f'8 ) |")
        >>> staff.append(r"abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> result = componenttools.copy_components_and_covered_spanners(
        ...     staff.leaves)
        >>> new_staff = Staff(result)

    ::

        >>> staff.leaves[0] is new_staff.leaves[0]
        False

    ::

        >>> show(new_staff) # doctest: +SKIP

    Copy `components` a total of `n` times:
    
    ::

        >>> result = componenttools.copy_components_and_covered_spanners(
        ...     staff.leaves[:2], n=4)
        >>> new_staff = Staff(result)

    ::

        >>> show(new_staff) # doctest: +SKIP

    Return new components.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools
    from abjad.tools import spannertools
    from abjad.tools.componenttools._set_component_parents_to_none \
        import _set_component_parents_to_none
    from abjad.tools.componenttools._restore_component_parents \
        import _restore_component_parents

    # check input
    assert componenttools.all_are_thread_contiguous_components(components)

    # return empty list when nothing to copy
    if n < 1:
        return []

    # copy components without spanners
    new_components = [
        component._copy_with_children_and_marks_but_without_spanners() 
        for component in components]
    new_components = type(components)(new_components)

    # make schema of spanners covered by components
    schema = spannertools.make_covered_spanner_schema(components)

    # copy spanners covered by components
    for covered_spanner, component_indices in schema.items():
        new_covered_spanner = copy.copy(covered_spanner)
        del(schema[covered_spanner])
        schema[new_covered_spanner] = component_indices

    # reverse schema
    reversed_schema = {}
    for new_covered_spanner, component_indices in schema.items():
        for component_index in component_indices:
            try:
                reversed_schema[component_index].append(new_covered_spanner)
            except KeyError:
                reversed_schema[component_index] = [new_covered_spanner]

    # iterate components and add new components to new spanners
    for component_index, new_component in enumerate(
        iterationtools.iterate_components_in_expr(new_components)):
        try:
            new_covered_spanners = reversed_schema[component_index]
            for new_covered_spanner in new_covered_spanners:
                new_covered_spanner.append(new_component)
        except KeyError:
            pass

    # repeat as specified by input
    for i in range(n - 1):
        new_components += copy_components_and_covered_spanners(components)

    # return new components
    return new_components
