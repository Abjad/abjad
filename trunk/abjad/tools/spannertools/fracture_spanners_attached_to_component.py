def fracture_spanners_attached_to_component(component, direction=None, klass=None):
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

        >>> parts = spannertools.fracture_spanners_attached_to_component(staff[1], Right)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8 ] )
            e'8 [ (
            f'8 ] ) \stopTrillSpan
        }

    Set `direction` to ``Left``, ``Right`` or ``None``.
    '''

    result = []
    for spanner in component.spanners:
        if klass is None:
            result.append(spanner.fracture(spanner.index(component), direction))
        elif isinstance(spanner, klass):
            result.append(spanner.fracture(spanner.index(component), direction))
    result.sort()
    return result
