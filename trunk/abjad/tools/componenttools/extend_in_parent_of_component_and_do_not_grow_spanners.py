def extend_in_parent_of_component_and_do_not_grow_spanners(component, new_components):
    r'''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.extend_in_parent_of_component()`` instead.

    Extend `components` in parent of `component` and do not grow spanners::

        >>> voice = Voice("c'8 [ d'8 e'8 ]")

    ::

        >>> notes = [Note("c'8"), Note("d'8"), Note("e'8")]
        >>> componenttools.extend_in_parent_of_component_and_do_not_grow_spanners(voice[-1], notes)
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

    Return list of `component` and `new_components`.

    .. versionchanged:: 2.0
        renamed ``extend_in_parent()`` to
        ``extend_in_parent_of_component_and_do_not_grow_spanners()``.
    '''
    from abjad.tools import componenttools

#    assert componenttools.all_are_components(new_components)
#
#    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])
#    if parent is not None:
#        after = stop + 1
#        # to avoid slice assignment pychecker errors
#        #parent[after:after] = new_components
#        parent.__setitem__(slice(after, after), new_components)
#
#    return [component] + new_components

    return componenttools.extend_in_parent_of_component(component, new_components, grow_spanners=False)
