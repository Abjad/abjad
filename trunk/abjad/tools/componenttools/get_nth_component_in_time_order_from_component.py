from abjad.tools import mathtools


def get_nth_component_in_time_order_from_component(component, n):
    r'''.. versionadded:: 2.9

    Get nth component from `component` in temporal order::

        >>> staff = Staff(r"c'4 \times 2/3 { d'8 e'8 f'8 } g'2")

    ::

        >>> f(staff)
        \new Staff {
            c'4
            \times 2/3 {
                d'8
                e'8
                f'8
            }
            g'2
        }

    ::

        >>> staff.leaves[1]
        Note("d'8")

    Return component right of `component` for positive `n`::

        >>> componenttools.get_nth_component_in_time_order_from_component(
        ...     staff.leaves[1], 1)
        Note("e'8")

    ::

        >>> componenttools.get_nth_component_in_time_order_from_component(
        ...     staff.leaves[1], 2)
        Note("f'8")

    ::

        >>> componenttools.get_nth_component_in_time_order_from_component(
        ...     staff.leaves[1], 3)
        Note("g'2")

    Return component left of `component` for negative `n`::

        >>> componenttools.get_nth_component_in_time_order_from_component(
        ...     staff.leaves[1], -1)
        Note("c'4")

    Return `component` when `n` is ``0``::

        >>> componenttools.get_nth_component_in_time_order_from_component(
        ...     staff.leaves[1], 0)
        Note("d'8")

    Return none when `n` is out of range::

        >>> componenttools.get_nth_component_in_time_order_from_component(
        ...     staff.leaves[1], 99) is None
        True

    Return none when `component` has no parent::

        >>> componenttools.get_nth_component_in_time_order_from_component(
        ...     staff, 1) is None
        True

    Return component or none.
    '''
    from abjad.tools import componenttools
    
    assert isinstance(component, componenttools.Component)
    assert mathtools.is_integer_equivalent_expr(n)

    def _next(component):
        for parent in componenttools.get_improper_parentage_of_component(component):
            next_sibling = componenttools.get_nth_sibling_from_component(parent, 1)
            if next_sibling is not None:
                return next_sibling

    def _prev(component):
        for parent in componenttools.get_improper_parentage_of_component(component):
            next_sibling = componenttools.get_nth_sibling_from_component(parent, -1)
            if next_sibling is not None:
                return next_sibling

    result = component

    if 0 < n:
        for i in range(n):
            result = _next(result)
    elif n < 0:
        for i in range(abs(n)):
            result = _prev(result)

    return result 
