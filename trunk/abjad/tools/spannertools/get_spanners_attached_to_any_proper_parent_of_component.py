from abjad.tools import componenttools


def get_spanners_attached_to_any_proper_parent_of_component(
    component, spanner_classes=None):
    r'''.. versionadded:: 2.0

    Get all spanners attached to any proper parent of `component`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner(staff.leaves)
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

        >>> spannertools.get_spanners_attached_to_any_proper_parent_of_component(
        ...     staff[0])
        set([TrillSpanner({c'8, d'8, e'8, f'8})])

    Return unordered set of zero or more spanners.
    '''
    from abjad.tools import spannertools

    # check input
    spanner_classes = spanner_classes or (spannertools.Spanner, )
    if not isinstance(spanner_classes, tuple):
        spanner_classes = (spanner_classes, )
    assert isinstance(spanner_classes, tuple)

    # initialize result set
    result = set([])

    # iterate parents
    for parent in component.select_parentage(include_self=False):
        for spanner in parent.spanners:
            for spanner_class in spanner_classes:
                if isinstance(spanner, spanner_class):
                    result.add(spanner)

    # return result
    return result
