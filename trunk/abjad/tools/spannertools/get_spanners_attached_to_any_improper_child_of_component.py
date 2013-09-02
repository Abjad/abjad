# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def get_spanners_attached_to_any_improper_child_of_component(
    component, spanner_classes=None):
    r'''Get all spanners attached to any improper children of `component`.

    ::

        >>> container = Container("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner(container.select_leaves())
        >>> first_slur = spannertools.SlurSpanner(container.select_leaves()[:2])
        >>> second_slur = spannertools.SlurSpanner(container.select_leaves()[2:])
        >>> trill = spannertools.TrillSpanner(container)
        >>> show(container) # doctest: +SKIP

    ..  doctest::

        >>> f(container)
        {
            c'8 [ ( \startTrillSpan
            d'8 )
            e'8 (
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> len(
        ...     spannertools.get_spanners_attached_to_any_improper_child_of_component(
        ...     container))
        4

    Get all spanners of `spanner_classes` attached to any proper children 
    of `component`:

    ::

        >>> spanner_classes = (spannertools.SlurSpanner, )
        >>> result = \
        ...     spannertools.get_spanners_attached_to_any_proper_child_of_component(
        ...     container, spanner_classes=spanner_classes)

    ::

        >>> list(sorted(result))
        [SlurSpanner(c'8, d'8), SlurSpanner(e'8, f'8)]

    Get all spanners of `spanner_classes` attached to any proper children 
    of `component`:

    ::

        >>> spanner_classes = (spannertools.SlurSpanner, spannertools.BeamSpanner)
        >>> result = \
        ...     spannertools.get_spanners_attached_to_any_proper_child_of_component(
        ...     container, spanner_classes=spanner_classes)

    ::

        >>> for spanner in list(sorted(result)):
        ...     spanner
        BeamSpanner(c'8, d'8, e'8, f'8)
        SlurSpanner(c'8, d'8)
        SlurSpanner(e'8, f'8)

    Return unordered set of zero or more spanners.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import spannertools

    # check input
    spanner_classes = spanner_classes or (spannertools.Spanner, )
    if not isinstance(spanner_classes, tuple):
        spanner_classes = (spanner_classes, )
    assert isinstance(spanner_classes, tuple)

    # initialize result set
    result = set([])

    # iterate children
    for child in iterationtools.iterate_components_in_expr([component]):
        spanners = child._get_spanners(spanner_classes)
        result.update(spanners)

    # return result
    return result
