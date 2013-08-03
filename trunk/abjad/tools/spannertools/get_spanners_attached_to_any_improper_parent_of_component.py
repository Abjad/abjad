# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def get_spanners_attached_to_any_improper_parent_of_component(
    component, spanner_classes=None):
    r'''Get all spanners attached to improper parentage of `component`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner(staff.select_leaves())
        >>> slur = spannertools.SlurSpanner(staff.select_leaves())
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
        ...     spannertools.get_spanners_attached_to_any_improper_parent_of_component(
        ...     staff[0])))

    ::

        >>> for spanner in result:
        ...     spanner
        ...
        BeamSpanner(c'8, d'8, e'8, f'8)
        SlurSpanner(c'8, d'8, e'8, f'8)
        TrillSpanner({c'8, d'8, e'8, f'8})

    Return unordered set of zero or more spanners.
    '''
    from abjad.tools import spannertools

    # check input
    spanner_classes = spanner_classes or (spannertools.Spanner, )
    if not isinstance(spanner_classes, tuple):
        spanner_classes = (spanner_classes, )
    assert isinstance(spanner_classes, tuple)

    # iterate parentage
    result = set([])
    for parent in component.select_parentage(include_self=True):
        for spanner in parent.get_spanners():
            for spanner_class in spanner_classes:
                if isinstance(spanner, spanner_class):
                    result.add(spanner)

    # return result
    return result
