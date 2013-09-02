# -*- encoding: utf-8 -*-


def get_the_only_spanner_attached_to_any_improper_parent_of_component(
    component, spanner_classes=None):
    r'''Get the only spanner attached to any improper parent `component`:

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

        >>> print spannertools.get_the_only_spanner_attached_to_any_improper_parent_of_component(
        ...     container)
        TrillSpanner({c'8, d'8, e'8, f'8})

    Raise missing spanner error when no spanner attached to `component`.

    Raise extra spanner error when more than one spanner attached to `component`.

    Return a single spanner.

    .. note:: function will usually be called with `spanner_classes` 
              specifier set.
    '''
    from abjad.tools import spannertools

    # get spanners and count spanners
    parent = component._get_parentage()
    spanners = parent._get_spanners(spanner_classes=spanner_classes)
    count = len(spanners)

    # raise or return
    if count == 0:
        raise MissingSpannerError
    elif count == 1:
        return spanners.pop()
    else:
        raise ExtraSpannerError
