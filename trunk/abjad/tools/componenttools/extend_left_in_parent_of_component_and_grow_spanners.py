def extend_left_in_parent_of_component_and_grow_spanners(component, new_components):
    r'''.. versionadded:: 2.0

    Extend `new_components` left in parent of `component` and grow spanners::

        abjad> voice = Voice("c'8 d'8 e'8")
        abjad> spannertools.BeamSpanner(voice[:])
        BeamSpanner(c'8, d'8, e'8)

    ::

        abjad> f(voice)
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }

    ::

        abjad> new_components = 3 * Note(0, (1, 16))
        abjad> componenttools.extend_left_in_parent_of_component_and_grow_spanners(voice[0], new_components)
        [Note("c'16"), Note("c'16"), Note("c'16"), Note("c'8")]

    ::

        abjad> f(voice)
        \new Voice {
            c'16 [
            c'16
            c'16
            c'8
            d'8
            e'8 ]
        }

    Return `new_components` and `component` together in newly created list.

    .. versionchanged:: 2.0
        renamed ``splice_left()`` to
        ``componenttools.extend_left_in_parent_of_component_and_grow_spanners()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import componenttools
    from abjad.tools import spannertools

    assert componenttools.all_are_components(new_components)
    offset = component._offset.start
    receipt = spannertools.get_spanners_that_dominate_components([component])
    for spanner, x in receipt:
        index = spannertools.find_index_of_spanner_component_at_score_offset(spanner, offset)
        for new_component in reversed(new_components):
            spanner._insert(index, new_component)
            new_component._spanners.add(spanner)
    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])
    if parent is not None:
        for new_component in reversed(new_components):
            new_component._parentage._switch(parent)
            parent._music.insert(start, new_component)
    return new_components + [component]
