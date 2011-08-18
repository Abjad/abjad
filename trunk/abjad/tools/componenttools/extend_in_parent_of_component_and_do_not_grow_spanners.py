from abjad.tools.componenttools.all_are_components import all_are_components
from abjad.tools.componenttools.get_parent_and_start_stop_indices_of_components import get_parent_and_start_stop_indices_of_components


def extend_in_parent_of_component_and_do_not_grow_spanners(component, components):
    r'''.. versionadded:: 1.1

    Extend `components` in parent of `component` and do not grow spanners::

        abjad> notes = [Note("c'8"), Note("d'8"), Note("e'8")]
        abjad> t = Voice("c'8 d'8 e'8")
        abjad> spannertools.BeamSpanner(t[:])
        BeamSpanner(c'8, d'8, e'8)
        abjad> notes = [Note("c'8"), Note("d'8"), Note("e'8")]
        abjad> componenttools.extend_in_parent_of_component_and_do_not_grow_spanners(t[-1], notes)
        [Note("e'8"), Note("c'8"), Note("d'8"), Note("e'8")]

    ::

        abjad> print t.format
        \new Voice {
            c'8 [
            d'8
            e'8 ]
            c'8
            d'8
            e'8
        }

    Return list of `component` and `components`.

    .. versionchanged:: 2.0
        renamed ``extend_in_parent()`` to
        ``extend_in_parent_of_component_and_do_not_grow_spanners()``.
    '''

    assert all_are_components(components)
    parent, start, stop = get_parent_and_start_stop_indices_of_components([component])
    if parent is not None:
        after = stop + 1
        parent[after:after] = components
    return [component] + components
