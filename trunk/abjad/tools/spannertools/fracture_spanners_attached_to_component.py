# -*- encoding: utf-8 -*-


def fracture_spanners_attached_to_component(
    component, direction=None, spanner_classes=None):
    r'''Fracture all spanners attached to `component` according to 
    `direction`.

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

        >>> parts = spannertools.fracture_spanners_attached_to_component(
        ...     container[1], direction=Right)
        >>> show(container) # doctest: +SKIP

    ..  doctest::

        >>> f(container)
        {
            c'8 [ ( \startTrillSpan
            d'8 ] )
            e'8 [ (
            f'8 ] ) \stopTrillSpan
        }

    Set `direction` to ``Left``, ``Right`` or ``None``.

    Return unordered set of fractured spanners.
    '''
    from abjad.tools import spannertools

    # initialize result set
    result = []

    # iterate spanners
    for spanner in spannertools.get_spanners_attached_to_component(
        component, spanner_classes=spanner_classes):
        result.append(spanner.fracture(spanner.index(component), direction))

    # return result
    return result
