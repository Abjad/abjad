def get_spanners_attached_to_component(component, klass=None):
    r'''.. versionadded:: 2.0

    Get all spanners attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = beamtools.BeamSpanner(staff.leaves)
        >>> first_slur = spannertools.SlurSpanner(staff.leaves[:2])
        >>> second_slur = spannertools.SlurSpanner(staff.leaves[2:])
        >>> crescendo = spannertools.CrescendoSpanner(staff.leaves)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ \< (
            d'8 )
            e'8 (
            f'8 ] \! )
        }

    ::

        >>> result = spannertools.get_spanners_attached_to_component(staff.leaves[0])
        >>> for x in sorted(result):
        ...     x
        ...
        BeamSpanner(c'8, d'8, e'8, f'8)
        CrescendoSpanner(c'8, d'8, e'8, f'8)
        SlurSpanner(c'8, d'8)

    Get spanners of `klass` attached to `component`::

        >>> klass = beamtools.BeamSpanner
        >>> result = spannertools.get_spanners_attached_to_component(staff.leaves[0], klass)
        >>> for x in sorted(result):
        ...     x
        ...
        BeamSpanner(c'8, d'8, e'8, f'8)

    Get spanners of any `klass` attached to `component`::

        >>> klasses = (beamtools.BeamSpanner, spannertools.SlurSpanner)
        >>> result = spannertools.get_spanners_attached_to_component(staff.leaves[0], klasses)
        >>> for x in sorted(result):
        ...     x
        ...
        BeamSpanner(c'8, d'8, e'8, f'8)
        SlurSpanner(c'8, d'8)

    Return unordered set of zero or more spanners.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_all_spanners_attached_to_component()`` to
        ``spannertools.get_spanners_attached_to_component()``.
    '''

    if klass is None:
        return component.spanners
    else:
        return set([x for x in component.spanners if isinstance(x, klass)])
