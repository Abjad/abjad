def fracture_spanners_attached_to_component(component, direction = 'both', klass = None):
    r'''.. versionadded:: 1.1

    Fracture all spanners attached to `component` according to `direction`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = beamtools.BeamSpanner(staff.leaves)
        >>> slur = spannertools.SlurSpanner(staff.leaves)
        >>> trill = spannertools.TrillSpanner(staff)
        >>> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> spannertools.fracture_spanners_attached_to_component(staff[1], 'right')
        [(BeamSpanner(c'8, d'8, e'8, f'8), BeamSpanner(c'8, d'8), BeamSpanner(e'8, f'8)), (SlurSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8))]

        >>> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8 ] )
            e'8 [ (
            f'8 ] ) \stopTrillSpan
        }

    Set `direction` to left, right or both.
    '''

    result = []
    #for spanner in set(component.spanners.attached):
    #for spanner in set(component.spanners._spanners):
    for spanner in component.spanners:
        if klass is None:
            result.append(spanner.fracture(spanner.index(component), direction))
        elif isinstance(spanner, klass):
            result.append(spanner.fracture(spanner.index(component), direction))
    result.sort()
    return result
