# -*- encoding: utf-8 -*-
def get_spanners_attached_to_component(component, spanner_classes=None):
    r'''Get all spanners attached to `component`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner(staff.select_leaves())
        >>> first_slur = spannertools.SlurSpanner(staff.select_leaves()[:2])
        >>> second_slur = spannertools.SlurSpanner(staff.select_leaves()[2:])
        >>> crescendo = spannertools.CrescendoSpanner(staff.select_leaves())

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 [ \< (
            d'8 )
            e'8 (
            f'8 ] \! )
        }

    ::

        >>> result = spannertools.get_spanners_attached_to_component(
        ...     staff.select_leaves()[0])
        >>> for x in sorted(result):
        ...     x
        ...
        BeamSpanner(c'8, d'8, e'8, f'8)
        CrescendoSpanner(c'8, d'8, e'8, f'8)
        SlurSpanner(c'8, d'8)

    Get spanners of `spanner_classes` attached to `component`:

    ::

        >>> spanner_classes = (spannertools.BeamSpanner, )
        >>> result = spannertools.get_spanners_attached_to_component(
        ...     staff.select_leaves()[0], spanner_classes=spanner_classes)
        >>> for x in sorted(result):
        ...     x
        ...
        BeamSpanner(c'8, d'8, e'8, f'8)

    Get spanners of `spanner_classes` attached to `component`:

    ::

        >>> spanner_classes = (spannertools.BeamSpanner, spannertools.SlurSpanner)
        >>> result = spannertools.get_spanners_attached_to_component(
        ...     staff.select_leaves()[0], spanner_classes=spanner_classes)
        >>> for x in sorted(result):
        ...     x
        ...
        BeamSpanner(c'8, d'8, e'8, f'8)
        SlurSpanner(c'8, d'8)

    Return unordered set of zero or more spanners.
    '''
    from abjad.tools import spannertools

    # check input
    spanner_classes = spanner_classes or (spannertools.Spanner, )
    if not isinstance(spanner_classes, tuple):
        spanner_classes = (spanner_classes, )
    assert isinstance(spanner_classes, tuple)

    # iterate spanners
    result = set()
    for spanner in component.spanners:
        if isinstance(spanner, spanner_classes):
            result.add(spanner)

    # return result
    return result
