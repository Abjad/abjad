from abjad.tools.containertools.Container import Container
from abjad.tools.componenttools.Component import Component


def insert_component_and_fracture_crossing_spanners(container, i, component):
    r'''Insert `component` into `container` at index `i` and fracture spanners::

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

        >>> parts = containertools.insert_component_and_fracture_crossing_spanners(staff, 1, Rest((1, 8)))

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ]
            r8
            d'8 [
            e'8
            f'8 ]
        }

    Return list of fractured spanners.

    .. versionchanged:: 2.0
        renamed ``containertools.insert_and_fracture()`` to
        ``containertools.insert_component_and_fracture_crossing_spanners()``.
    '''
    from abjad.tools import leaftools
    from abjad.tools import spannertools

    # check input
    assert isinstance(container, Container)
    assert isinstance(component, Component)
    assert isinstance(i, int)

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
