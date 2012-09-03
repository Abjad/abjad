def extend_in_parent_of_component(component, new_components, grow_spanners=True):
    r'''.. versionadded:: 2.10

    Extend `new_components` in parent of `component`.

    Example 1. Extend `new_component` in parent of `component`.
    Grow spanners:

        >>> voice = Voice("c'8 [ d'8 e'8 ]")

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }

    ::

        >>> new_components = [Note("c'8"), Note("d'8"), Note("e'8")]
        >>> componenttools.extend_in_parent_of_component(
        ...     voice.leaves[-1], new_components, grow_spanners=True)
        [Note("e'8"), Note("c'8"), Note("d'8"), Note("e'8")]

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8
            c'8
            d'8
            e'8 ]
        }

    Example 2. Extend `new_component` in parent of `component`.
    Do not grow spanners:

        >>> voice = Voice("c'8 [ d'8 e'8 ]")

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }

    ::
    
        >>> new_components = [Note("c'8"), Note("d'8"), Note("e'8")]
        >>> componenttools.extend_in_parent_of_component(
        ...     voice.leaves[-1], new_components, grow_spanners=False)
        [Note("e'8"), Note("c'8"), Note("d'8"), Note("e'8")]

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8 ]
            c'8
            d'8
            e'8
        }


    Return `component` and `new_components` together in newly constructed list.
    '''
    from abjad.tools import componenttools
    from abjad.tools import spannertools

    # check input
    assert componenttools.all_are_components(new_components)

    # extend spanners if required
    if grow_spanners:
        insert_offset = component.stop_offset
        receipt = spannertools.get_spanners_that_dominate_components([component])
        for spanner, index in receipt:
            insert_component = spannertools.find_spanner_component_starting_at_exactly_score_offset(
                spanner, insert_offset)
            if insert_component is not None:
                insert_index = spanner.index(insert_component)
            else:
                insert_index = len(spanner)
            for new_component in reversed(new_components):
                spanner._insert(insert_index, new_component)
                new_component._spanners.add(spanner)

    # find parent
    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])

    # extend new components in parent
    if parent is not None:
        if grow_spanners:
            for new_component in reversed(new_components):
                new_component._switch(parent)
                parent._music.insert(start + 1, new_component)
        else:
            after = stop + 1
            # to avoid slice assignment pychecker errors
            #parent[after:after] = new_components
            parent.__setitem__(slice(after, after), new_components)

    # return component and new components together
    return [component] + new_components
