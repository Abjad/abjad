def get_parent_and_start_stop_indices_of_components(components):
    r'''.. versionadded:: 1.1

    Get parent and start / stop indices of `components`::

        abjad> t = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
        abjad> print t.format
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }

    ::

        abjad> leaves = t[-2:]
        abjad> leaves
        [Note("g'8"), Note("a'8")]
        abjad> componenttools.get_parent_and_start_stop_indices_of_components(leaves)
        (Staff{6}, 4, 5)

    Return parent / start index / stop index triple. Return parent as component or none.
    Return nonnegative integer start index and nonnegative index stop index.

    .. versionchanged:: 2.0
        renamed ``componenttools.get_with_indices()`` to
        ``componenttools.get_parent_and_start_stop_indices_of_components()``.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components)

    if 0 < len(components):
        first, last = components[0], components[-1]
        parent = first._parentage.parent
        if parent is not None:
            first_index = parent.index(first)
            last_index = parent.index(last)
            return parent, first_index, last_index

    return None, None, None
