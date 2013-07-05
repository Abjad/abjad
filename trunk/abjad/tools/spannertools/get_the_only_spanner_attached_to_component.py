def get_the_only_spanner_attached_to_component(
    component, spanner_classes=None):
    r'''.. versionadded:: 1.1

    Get the only spanner attached to `component`:

    ::

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

        >>> print spannertools.get_the_only_spanner_attached_to_component(
        ...     staff)
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
