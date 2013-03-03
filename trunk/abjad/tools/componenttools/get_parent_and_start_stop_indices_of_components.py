def get_parent_and_start_stop_indices_of_components(components):
    r'''.. versionadded:: 1.1

    Get parent and start / stop indices of `components`::

        >>> t = Staff("c'8 d'8 e'8 f'8 g'8 a'8")

    ::

        >>> f(t)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }

    ::

        >>> leaves = t[-2:]
        >>> leaves
        Selection(Note("g'8"), Note("a'8"))
        >>> componenttools.get_parent_and_start_stop_indices_of_components(leaves)
        (Staff{6}, 4, 5)

    Return parent / start index / stop index triple. Return parent as component or none.
    Return nonnegative integer start index and nonnegative index stop index.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components)

    if 0 < len(components):
        first, last = components[0], components[-1]
        parent = first._parent
        if parent is not None:
            first_index = parent.index(first)
            last_index = parent.index(last)
            return parent, first_index, last_index

    return None, None, None
