# -*- encoding: utf-8 -*-


def detach_spanners_attached_to_component(component, spanner_classes=None):
    r'''Detach spanners of `spanner_classes` attached to `component`.

    ::

        >>> container = Container("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner(container.select_leaves())
        >>> slur = spannertools.SlurSpanner(container.select_leaves())
        >>> trill = spannertools.TrillSpanner(container)
        >>> show(container) # doctest: +SKIP

    ..  doctest::

        >>> f(container)
        {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> spanners = spannertools.detach_spanners_attached_to_component(
        ...     container[0])
        >>> show(container) # doctest: +SKIP

    ..  doctest::

        >>> f(container)
        {
            c'8 \startTrillSpan
            d'8
            e'8
            f'8 \stopTrillSpan
        }

    Detach all spanners when `spanner_classes` is none.

    Return unordered set of zero or more empty spanners.
    '''
    from abjad.tools import spannertools

    # check input
    spanner_classes = spanner_classes or (spannertools.Spanner, )
    if not isinstance(spanner_classes, tuple):
        spanner_classes = (spanner_classes, )

    # initialize result set
    result = set()

    # iterate spanners
    for spanner in component._get_spanners(spanner_classes):
        spanner.detach()
        result.add(spanner)

    # return result
    return result
