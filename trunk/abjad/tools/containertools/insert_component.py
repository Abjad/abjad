from abjad.tools import componenttools
from abjad.tools import leaftools


def insert_component(container, i, component, fracture_spanners=False):
    r'''.. versionadded:: 2.10

    Insert `component` into `container` at index `i`.

    Example 1.  Insert `component` into `container` at index `i`.
    Do not fracture crossing spanners::

        >>> staff = Staff("c'8 [ d'8 e'8 f'8 ]")

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> containertools.insert_component(staff, 1, Note("cs'8"), fracture_spanners=False)
        Staff{5}

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            cs'8
            d'8
            e'8
            f'8 ]
        }

    Example 2.  Insert `component` into `container` at index `i`.
    Fracture crossing spanners.

        >>> staff = Staff("c'8 [ d'8 e'8 f'8 ]")

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> parts = containertools.insert_component(staff, 1, Rest('r8'), fracture_spanners=True)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ]
            r8
            d'8 [
            e'8
            f'8 ]
        }

    Return `container` or list of fractured spanners.
    '''
    from abjad.tools import containertools
    from abjad.tools import spannertools

    # check input
    assert isinstance(container, containertools.Container)
    assert isinstance(component, componenttools.Component)
    assert isinstance(i, int)

    if not fracture_spanners:

        # insert component into container at index i
        # to avoid pychecker slice assignment error
        #container[i:i] = [component]
        container.__setitem__(slice(i, i), [component])

        # return container
        return container

    result = []
    component._switch(container)
    container._music.insert(i, component)

    previous_leaf = leaftools.get_nth_leaf_in_thread_from_leaf(component, -1)
    if previous_leaf:
        result.extend(spannertools.fracture_spanners_attached_to_component(previous_leaf, direction=Right))

    next_leaf = leaftools.get_nth_leaf_in_thread_from_leaf(component, 1)
    if next_leaf:
        result.extend(spannertools.fracture_spanners_attached_to_component(next_leaf, direction=Left))

    return result
