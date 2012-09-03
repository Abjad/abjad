def extend_left_in_parent_of_component_and_do_not_grow_spanners(component, new_components):
    r'''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.extend_left_in_parent_of_component()`` instead.

    Extend `new_components` left in parent of `component` and do not grow spanners::

        >>> voice = Voice("c'8 [ d'8 e'8 ]")

    ::

        >>> notes = [Note("c'8"), Note("d'8"), Note("e'8")]
        >>> componenttools.extend_left_in_parent_of_component_and_do_not_grow_spanners(voice[0], notes)
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

    .. versionchanged:: 2.0 renamed ``extend_left_in_parent()`` to
        ``extend_left_in_parent_of_component_and_do_not_grow_spanners()``.
    '''
    from abjad.tools import componenttools

#    assert componenttools.all_are_components(new_components)
#
#    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])
#
#    if parent is not None:
#        # to avoid slice assignment pychecker errors
#        #parent[start:start] = new_components
#        parent.__setitem__(slice(start, start), new_components)
#
#    return new_components + [component]

    return componenttools.extend_left_in_parent_of_component(component, new_components, grow_spanners=False)
