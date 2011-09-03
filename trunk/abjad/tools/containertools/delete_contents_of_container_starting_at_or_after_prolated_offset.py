from abjad.tools.containertools.get_first_element_starting_at_or_after_prolated_offset import get_first_element_starting_at_or_after_prolated_offset


def delete_contents_of_container_starting_at_or_after_prolated_offset(container, prolated_offset):
    r'''.. versionadded:: 2.0

    Delete contents of `container` starting at or after `prolated_offset`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        abjad> containertools.delete_contents_of_container_starting_at_or_after_prolated_offset(staff, Duration(1, 8))
        Staff{1}

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ]
        }

    Return `container`.

    .. versionchanged:: 2.0
        renamed ``containertools.contents_delete_starting_not_before_prolated_offset()`` to
        ``containertools.delete_contents_of_container_starting_at_or_after_prolated_offset()``.
    '''

    # get start element
    element = get_first_element_starting_at_or_after_prolated_offset(container, prolated_offset)

    # get start index
    index = container.index(element)

    # delete elements in container starting not before index
    del(container[index:])

    # return container minus deleted contents
    return container
