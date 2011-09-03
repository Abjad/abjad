from abjad.tools.containertools.get_first_element_starting_strictly_after_prolated_offset import get_first_element_starting_strictly_after_prolated_offset


def delete_contents_of_container_starting_strictly_after_prolated_offset(container, prolated_offset):
    r'''.. versionadded:: 2.0

    Delete contents of `container` starting strictly after `prolated_offset`::

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

        abjad> containertools.delete_contents_of_container_starting_strictly_after_prolated_offset(staff, Duration(1, 8))
        Staff{2}

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
        }

    Return `container`.

    .. versionchanged:: 2.0
        renamed ``containertools.contents_delete_starting_after_prolated_offset()`` to
        ``containertools.delete_contents_of_container_starting_strictly_after_prolated_offset()``.
    '''

    # get index
    try:
        element = get_first_element_starting_strictly_after_prolated_offset(container, prolated_offset)
        index = container.index(element)

    # return container if no index
    except ValueError:
        return container

    # delete elements
    del(container[index:])

    # return container
    return container
