from abjad.tools import componenttools


def get_spanners_attached_to_any_improper_parent_of_component(component, klass=None):
    r'''.. versionadded:: 1.1

    Get all spanners attached to improper parentage of `component`::

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

        >>> result = list(sorted(
        ... spannertools.get_spanners_attached_to_any_improper_parent_of_component(staff[0])))

    ::

        >>> for spanner in result:
        ...     spanner
        ...
        BeamSpanner(c'8, d'8, e'8, f'8)
        SlurSpanner(c'8, d'8, e'8, f'8)
        TrillSpanner({c'8, d'8, e'8, f'8})

    Return unordered set of zero or more spanners.
    '''
    # externalized version of (old) spanner receptor 'spanners_in_parentage' attribute
    result = set([])
    parentage = componenttools.get_improper_parentage_of_component(component)
    for parent in parentage:
        for spanner in parent.spanners:
            if klass is None:
                result.add(spanner)
            elif isinstance(spanner, klass):
                result.add(spanner)
    return result
