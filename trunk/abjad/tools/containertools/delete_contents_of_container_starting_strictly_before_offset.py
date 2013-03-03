def delete_contents_of_container_starting_strictly_before_offset(container, prolated_offset):
    r'''.. versionadded:: 2.0

    Delete contents of `container` contents starting strictly before `prolated_offset`::

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

        >>> containertools.delete_contents_of_container_starting_strictly_before_offset(
        ...     staff, Duration(1, 8))
        Staff{3}

    ::

        >>> f(staff)
        \new Staff {
            d'8 [
            e'8
            f'8 ]
        }

    Return `container`.
    '''
    from abjad.tools import containertools

    # get index
    try:
        element = containertools.get_first_element_starting_strictly_before_offset(
            container, prolated_offset)
        index = container.index(element)

    # return container if no index
    except ValueError:
        return container

    # delete elements
    del(container[:index+1])

    # return container
    return container
