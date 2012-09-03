def extend_left_in_parent_of_component(component, new_components, grow_spanners=True):
    r'''.. versionadded:: 2.10

    Extend `new_components` left in parent of `component`.

    Example 1. Extend `new_components` left in parent of `component`.
    Grow spanners::

        >>> voice = Voice("c'8 [ d'8 e'8 ]")

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }

    ::

        >>> notes = [Note("c'8"), Note("d'8"), Note("e'8")]
        >>> componenttools.extend_left_in_parent_of_component(
        ...     voice[0], notes, grow_spanners=True)
        [Note("c'8"), Note("d'8"), Note("e'8"), Note("c'8")]

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

    Example 2. Extend `new_components` left in parent of `component`.
    Do not grow spanners::

        >>> voice = Voice("c'8 [ d'8 e'8 ]")

    ::

        >>> notes = [Note("c'8"), Note("d'8"), Note("e'8")]
        >>> componenttools.extend_left_in_parent_of_component(
        ...     voice[0], notes, grow_spanners=False)
        [Note("c'8"), Note("d'8"), Note("e'8"), Note("c'8")]

    ::

        >>> f(voice)
        \new Voice {
            c'8
            d'8
            e'8
            c'8 [
            d'8
            e'8 ]
        }

    Return `new_components` and `component` together in newly created list.
    '''
    from abjad.tools import componenttools
    from abjad.tools import spannertools

    assert componenttools.all_are_components(new_components)

    if grow_spanners:
        offset = component.start_offset
        receipt = spannertools.get_spanners_that_dominate_components([component])
        for spanner, x in receipt:
            index = spannertools.find_index_of_spanner_component_at_score_offset(spanner, offset)
            for new_component in reversed(new_components):
                spanner._insert(index, new_component)
                new_component._spanners.add(spanner)

    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])

    if parent is not None:
        if grow_spanners:
            for new_component in reversed(new_components):
                new_component._switch(parent)
                parent._music.insert(start, new_component)
        else:
            # to avoid slice assignment pychecker errors
            #parent[start:start] = new_components
            parent.__setitem__(slice(start, start), new_components)

    return new_components + [component]
