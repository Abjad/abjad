def delete_contents_of_container_starting_at_or_after_offset(container, prolated_offset):
    r'''.. versionadded:: 2.0

    Delete contents of `container` starting at or after `prolated_offset`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> containertools.delete_contents_of_container_starting_at_or_after_offset(
        ...     staff, Duration(1, 8))
        Staff{1}

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ]
        }

    Return `container`.
    '''
    from abjad.tools import containertools

    # get start element
    element = containertools.get_first_element_starting_at_or_after_offset(container, prolated_offset)

    # get start index
    index = container.index(element)

    # delete elements in container starting not before index
    del(container[index:])

    # return container minus deleted contents
    return container
