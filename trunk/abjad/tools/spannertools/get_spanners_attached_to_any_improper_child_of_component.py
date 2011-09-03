from abjad.tools.spannertools.get_spanners_attached_to_component import get_spanners_attached_to_component


def get_spanners_attached_to_any_improper_child_of_component(component, klass = None):
    r'''.. versionadded:: 2.0

    Get all spanners attached to any improper children of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = spannertools.BeamSpanner(staff.leaves)
        abjad> first_slur = spannertools.SlurSpanner(staff.leaves[:2])
        abjad> second_slur = spannertools.SlurSpanner(staff.leaves[2:])
        abjad> trill = spannertools.TrillSpanner(staff)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8 )
            e'8 (
            f'8 ] ) \stopTrillSpan
        }

    ::

        abjad> len(spannertools.get_spanners_attached_to_any_improper_child_of_component(staff)) == 4
        True

    Get all spanners of `klass` attached to any proper children of `component`::

        abjad> spanner_klass = spannertools.SlurSpanner
        abjad> spannertools.get_spanners_attached_to_any_proper_child_of_component(staff, spanner_klass) # doctest: +SKIP
        set([SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)])

    Get all spanners of any `klass` attached to any proper children of `component`::

        abjad> spanner_klasses = (spannertools.SlurSpanner, spannertools.BeamSpanner)
        abjad> spannertools.get_spanners_attached_to_any_proper_child_of_component(staff, spanner_klasses) # doctest: +SKIP
        set([BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)])

    Return unordered set of zero or more spanners.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_all_spanners_attached_to_any_improper_children_of_component()`` to
        ``spannertools.get_spanners_attached_to_any_improper_child_of_component()``.
    '''
    from abjad.tools.componenttools._Component import _Component
    from abjad.tools import componenttools

    # note: externalization of (old) component spanner aggregator 'contained' property
    result = set([])

    # inspect component itself
    result.update(get_spanners_attached_to_component(component, klass))

    # iterate proper children of component
    children = componenttools.iterate_components_forward_in_expr(component, _Component)
    for child in children:
        result.update(get_spanners_attached_to_component(child, klass))

    # return result
    return result



