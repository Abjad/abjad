# -*- encoding: utf-8 -*-
def detach_spanners_attached_to_components_in_expr(
    expr, spanner_classes=None):
    r'''Destroy spanners of `spanner_classes` attached to components in `expr`:

    ::

        >>> staff = Staff("c'4 [ ( d' e' f' ) ]")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4 [ (
            d'4
            e'4
            f'4 ] )
        }

    ::

        >>> spanners = \
        ...     spannertools.detach_spanners_attached_to_components_in_expr(
        ...     staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return unordered set of zero or more empty spanners.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import spannertools

    # check input
    spanner_classes = spanner_classes or (spannertools.Spanner, )
    if not isinstance(spanner_classes, tuple):
        spanner_classes = (spanner_classes, )
    assert isinstance(spanner_classes, tuple)

    # initialize result set
    result = set()

    # iterate components
    for component in iterationtools.iterate_components_in_expr(expr):
        result.update(spannertools.detach_spanners_attached_to_component(
            component, spanner_classes=spanner_classes))

    # return result
    return result
