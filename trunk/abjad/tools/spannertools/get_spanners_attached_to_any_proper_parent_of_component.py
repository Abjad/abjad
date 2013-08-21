# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def get_spanners_attached_to_any_proper_parent_of_component(
    component, spanner_classes=None):
    r'''Get all spanners attached to any proper parent of `component`.

    ::

        >>> container = Container("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner(container.select_leaves())
        >>> slur = spannertools.SlurSpanner(container.select_leaves())
        >>> trill = spannertools.TrillSpanner(container)
        >>> f(container)
        {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> spannertools.get_spanners_attached_to_any_proper_parent_of_component(
        ...     container[0])
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
    for parent in component._get_parentage(include_self=False):
        for spanner in parent._get_spanners():
            for spanner_class in spanner_classes:
                if isinstance(spanner, spanner_class):
                    result.add(spanner)

    # return result
    return result
