from abjad.tools.spannertools.get_spanners_attached_to_component import get_spanners_attached_to_component


def get_spanners_attached_to_any_proper_child_of_component(component, klass=None):
    r'''.. versionadded:: 2.0

    Get all spanners attached to any proper children of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = beamtools.BeamSpanner(staff.leaves)
        >>> first_slur = spannertools.SlurSpanner(staff.leaves[:2])
        >>> second_slur = spannertools.SlurSpanner(staff.leaves[2:])
        >>> trill = spannertools.TrillSpanner(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8 )
            e'8 (
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> len(spannertools.get_spanners_attached_to_any_proper_child_of_component(staff)) == 3
        True

    Get all spanners of `klass` attached to any proper children of `component`::

        >>> spanner_klass = spannertools.SlurSpanner
        >>> spannertools.get_spanners_attached_to_any_proper_child_of_component(staff, spanner_klass) # doctest: +SKIP
        set([SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)])

    Get all spanners of any `klass` attached to any proper children of `component`::

        >>> spanner_klasses = (spannertools.SlurSpanner, beamtools.BeamSpanner)
        >>> spannertools.get_spanners_attached_to_any_proper_child_of_component(staff, spanner_klasses) # doctest: +SKIP
        set([BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)])

    Return unordered set of zero or more spanners.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_all_spanners_attached_to_any_proper_children_of_component()`` to
        ``spannertools.get_spanners_attached_to_any_proper_child_of_component()``.
    '''
    from abjad.tools import componenttools

    # note: externalization of (old) component spanner aggregator 'children' property
    result = set([])
    components = componenttools.iterate_components_forward_in_expr(component)

    # remove component itself from iteration
    components.next()

    # iterate only proper children of component and save spanners
    for component in components:
        result.update(get_spanners_attached_to_component(component, klass))

    # return result
    return result
