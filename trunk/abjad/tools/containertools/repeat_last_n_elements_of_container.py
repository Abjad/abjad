from abjad.tools.componenttools.copy_components_and_immediate_parent_of_first_component import copy_components_and_immediate_parent_of_first_component


def repeat_last_n_elements_of_container(container, n = 1, total = 2):
    r'''.. versionadded:: 1.1

    Repeat last `n` elements of `container`::

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

        abjad> containertools.repeat_last_n_elements_of_container(staff, n = 2, total = 3)
        Staff{8}

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            e'8 [
            f'8 ]
            e'8 [
            f'8 ]
        }

    Return `container`.

    .. versionchanged:: 2.0
        renamed ``containertools.extend_cyclic()`` to
        ``containertools.repeat_last_n_elements_of_container()``.
    '''

    # get start and stop indices
    stop = len(container)
    start = stop - n

    # for the total number of elements less one
    for x in range(total - 1):

        # copy last n elements of container
        addendum = copy_components_and_immediate_parent_of_first_component(container[start:stop])

        # extend container with addendum
        container.extend(addendum)

    return container
