# -*- encoding: utf-8 -*-
def fracture_spanners_attached_to_component(
    component, direction=None, spanner_classes=None):
    r'''Fracture all spanners attached to `component` according to `direction`:

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

        >>> parts = spannertools.fracture_spanners_attached_to_component(
        ...     staff[1], direction=Right)

    ..  doctest::

        >>> f(staff)
        \new Staff {
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
