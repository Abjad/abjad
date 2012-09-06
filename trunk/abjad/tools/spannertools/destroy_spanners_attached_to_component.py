def destroy_spanners_attached_to_component(component, klass=None):
    r'''.. versionadded:: 1.1

    Destroy spanners of `klass` attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = beamtools.BeamSpanner(staff.leaves)
        >>> slur = spannertools.SlurSpanner(staff.leaves)
        >>> trill = spannertools.TrillSpanner(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> spanners = spannertools.destroy_spanners_attached_to_component(staff[0])

    ::

        >>> f(staff)
        \new Staff {
            c'8 \startTrillSpan
            d'8
            e'8
            f'8 \stopTrillSpan
        }

    Destroy all spanners when `klass` is none.

    Return tuple of zero or more empty spanners.

    Order of spanners in return value can not be predicted.
    '''
    from abjad.tools import spannertools

    result = []
    for spanner in spannertools.get_spanners_attached_to_component(component):
        if klass is None or isinstance(spanner, klass):
            spanner.clear()
            result.append(spanner)

    return tuple(result)
