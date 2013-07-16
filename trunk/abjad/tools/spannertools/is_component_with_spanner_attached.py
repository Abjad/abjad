from abjad.tools import componenttools


def is_component_with_spanner_attached(expr, spanner_classes=None):
    r'''.. versionadded:: 2.0

    True when `expr` is a component with spanner attached:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = spannertools.BeamSpanner(staff.select_leaves())
        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> spannertools.is_component_with_spanner_attached(staff[0])
        True

    Otherwise false:

    ::

        >>> spannertools.is_component_with_spanner_attached(staff)
        False

    When `spanner_classes` is not none then true when `expr` is a component
    with a spanner of `spanner_classes` attached.

    Return true or false.
    '''
    from abjad.tools import spannertools

    if isinstance(expr, componenttools.Component):
        spanners = spannertools.get_spanners_attached_to_component(
            expr, spanner_classes=spanner_classes)

        return bool(spanners)

    return False
