from abjad.tools.containertools.Container import Container
from abjad.tools.componenttools._Component import _Component


def insert_component_and_fracture_crossing_spanners(container, i, component):
    r'''Insert `component` into `container` at index `i` and fracture spanners::

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

        abjad> containertools.insert_component_and_fracture_crossing_spanners(staff, 1, Rest((1, 8)))
        [(BeamSpanner(c'8, d'8, e'8, f'8), BeamSpanner(c'8), BeamSpanner(d'8, e'8, f'8)), (BeamSpanner(d'8, e'8, f'8), BeamSpanner(), BeamSpanner(d'8, e'8, f'8))]

    ::

        abjad> f(staff)
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
    from abjad.tools import spannertools

    if not isinstance(container, Container):
        raise TypeError('must be container: %s' % container)

    assert isinstance(i, int)
    assert isinstance(component, _Component)

    result = []
    component._parentage._switch(container)
    container._music.insert(i, component)
    if component._navigator._prev_bead:
        result.extend(spannertools.fracture_all_spanners_attached_to_component(
            component._navigator._prev_bead, direction = 'right'))
    if component._navigator._next_bead:
        result.extend(spannertools.fracture_all_spanners_attached_to_component(
            component._navigator._next_bead, direction = 'left'))

    return result
