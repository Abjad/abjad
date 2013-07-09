def extend_in_parent_of_component(
    component, new_components, left=False, grow_spanners=True):
    r'''.. versionadded:: 2.10

    Extend `new_components` in parent of `component`.

    Example 1. Extend `new_component` in parent of `component`.
    Grow spanners:

    ::

        >>> staff = Staff(r"c'8 ( d'8 e'8 f'8 )")
        >>> time_signature = contexttools.TimeSignatureMark((2, 4))
        >>> time_signature.attach(staff)
        TimeSignatureMark((2, 4))(Staff{4})

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> new_components = [Note("g'4"), Note("fs'4")]

    ::

        >>> result = componenttools.extend_in_parent_of_component(
        ...     staff.leaves[-1], 
        ...     new_components,
        ...     grow_spanners=True)

    ::

        >>> show(staff) # doctest: +SKIP


    Example 2. Extend `new_component` in parent of `component`.  
    Do not grow spanners:

    ::

        >>> staff = Staff(r"c'8 ( d'8 e'8 f'8 )")
        >>> time_signature = contexttools.TimeSignatureMark((2, 4))
        >>> time_signature.attach(staff)
        TimeSignatureMark((2, 4))(Staff{4})

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> new_components = [Note("g'4"), Note("fs'4")]

    ::

        >>> result = componenttools.extend_in_parent_of_component(
        ...     staff.leaves[-1], 
        ...     new_components,
        ...     grow_spanners=False)

    ::

        >>> show(staff) # doctest: +SKIP

    Example 3. Extend `new_components` left in parent of `component`.
    Grow spanners:

    ::

        >>> staff = Staff(r"c'8 ( d'8 e'8 f'8 )")
        >>> time_signature = contexttools.TimeSignatureMark((2, 4))
        >>> time_signature.attach(staff)
        TimeSignatureMark((2, 4))(Staff{4})

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> new_components = [Note("g'4"), Note("fs'4")]

    ::

        >>> result = componenttools.extend_in_parent_of_component(
        ...     staff.leaves[0], 
        ...     new_components,
        ...     left=True,
        ...     grow_spanners=True)

    ::

        >>> show(staff) # doctest: +SKIP

    Example 4. Extend `new_components` left in parent of `component`.
    Do not grow spanners:

    ::

        >>> staff = Staff(r"c'8 ( d'8 e'8 f'8 )")
        >>> time_signature = contexttools.TimeSignatureMark((2, 4))
        >>> time_signature.attach(staff)
        TimeSignatureMark((2, 4))(Staff{4})

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> new_components = [Note("g'4"), Note("fs'4")]

    ::

        >>> result = componenttools.extend_in_parent_of_component(
        ...     staff.leaves[0], 
        ...     new_components,
        ...     left=True,
        ...     grow_spanners=False)

    ::

        >>> show(staff) # doctest: +SKIP

    Return `component` and `new_components` together in newly 
    constructed list.
    '''
    from abjad.tools import componenttools
    from abjad.tools import spannertools

    # check input
    assert componenttools.all_are_components(new_components)

    # extend to the right of component
    if not left:

        # extend spanners if required
        if grow_spanners:
            insert_offset = component.timespan.stop_offset
            receipt = spannertools.get_spanners_that_dominate_components(
                [component])
            for spanner, index in receipt:
                insert_component = \
                    spannertools.find_spanner_component_starting_at_exactly_score_offset(
                    spanner, insert_offset)
                if insert_component is not None:
                    insert_index = spanner.index(insert_component)
                else:
                    insert_index = len(spanner)
                for new_component in reversed(new_components):
                    spanner._insert(insert_index, new_component)
                    new_component._spanners.add(spanner)

        # find parent
        parent, start, stop = \
            componenttools.get_parent_and_start_stop_indices_of_components(
            [component])

        # extend new components in parent
        if parent is not None:
            if grow_spanners:
                for new_component in reversed(new_components):
                    new_component._set_parent(parent)
                    parent._music.insert(start + 1, new_component)
            else:
                after = stop + 1
                # to avoid slice assignment pychecker errors
                #parent[after:after] = new_components
                parent.__setitem__(slice(after, after), new_components)

        # return component and new components together
        return [component] + new_components

    # extend to the left of component
    else:

        if grow_spanners:
            offset = component.timespan.start_offset
            receipt = spannertools.get_spanners_that_dominate_components(
                [component])
            for spanner, x in receipt:
                index = \
                    spannertools.find_index_of_spanner_component_at_score_offset(
                    spanner, offset)
                for new_component in reversed(new_components):
                    spanner._insert(index, new_component)
                    new_component._spanners.add(spanner)

        parent, start, stop = \
            componenttools.get_parent_and_start_stop_indices_of_components(
            [component])

        if parent is not None:
            if grow_spanners:
                for new_component in reversed(new_components):
                    new_component._set_parent(parent)
                    parent._music.insert(start, new_component)
            else:
                parent.__setitem__(slice(start, start), new_components)

        return new_components + [component]
