# -*- encoding: utf-8 -*-
def detach_spanners_attached_to_component(component, spanner_classes=None):
    r'''Destroy spanners of `spanner_classes` attached to `component`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner(staff.select_leaves())
        >>> slur = spannertools.SlurSpanner(staff.select_leaves())
        >>> trill = spannertools.TrillSpanner(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> spanners = spannertools.detach_spanners_attached_to_component(
        ...     staff[0])

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 \startTrillSpan
            d'8
            e'8
            f'8 \stopTrillSpan
        }

    Destroy all spanners when `spanner_classes` is none.

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
    for spanner in spannertools.get_spanners_attached_to_component(
        component, spanner_classes=spanner_classes):
            spanner.detach()
            result.add(spanner)

    # return result
    return result
