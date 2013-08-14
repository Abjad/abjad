# -*- encoding: utf-8 -*-


def get_the_only_spanner_attached_to_component(
    component, spanner_classes=None):
    r'''Get the only spanner attached to `component`.

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

        >>> print spannertools.get_the_only_spanner_attached_to_component(
        ...     container)
        TrillSpanner({c'8, d'8, e'8, f'8})

    Raise missing spanner error when no spanner attached to `component`.

    Raise extra spanner error when more than one spanner attached 
    to `component`.

    Return a single spanner.

    .. note:: function will usually be called with `spanner_classes` 
              specifier set.
    '''
    from abjad.tools import spannertools

    # check input
    spanner_classes = spanner_classes or (spannertools.Spanner, )
    if not isinstance(spanner_classes, tuple):
        spanner_classes = (spanner_classes, )
    assert isinstance(spanner_classes, tuple)

    # get spanners
    spanners = spannertools.get_spanners_attached_to_component(
        component, spanner_classes=spanner_classes)

    # count spanners
    count = len(spanners)

    # raise or return
    if count == 0:
        raise MissingSpannerError
    elif count == 1:
        return spanners.pop()
    else:
        raise ExtraSpannerError
