def get_spanners_attached_to_any_proper_parent_of_component(component, klass = None):
    r'''.. versionadded:: 2.0

    Get all spanners attached to any proper parent of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = spannertools.BeamSpanner(staff.leaves)
        abjad> slur = spannertools.SlurSpanner(staff.leaves)
        abjad> trill = spannertools.TrillSpanner(staff)
        abjad> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        abjad> spannertools.get_spanners_attached_to_any_proper_parent_of_component(staff[0])
        set([TrillSpanner({c'8, d'8, e'8, f'8})])

    Return unordered set of zero or more spanners.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_all_spanners_attached_to_any_proper_parent_of_component( )`` to
        ``spannertools.get_spanners_attached_to_any_proper_parent_of_component( )``.
    '''
    from abjad.tools import componenttools

    result = set([ ])
    parentage = componenttools.get_proper_parentage_of_component(component)
    for parent in parentage:
        for spanner in parent.spanners:
            if klass is None:
                result.add(spanner)
            elif isinstance(spanner, klass):
                result.add(spanner)
    return result



