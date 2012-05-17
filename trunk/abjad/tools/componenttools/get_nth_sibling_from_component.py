def get_nth_sibling_from_component(component, n):
    r'''.. versionadded:: 2.9

    Get nth sibling from `component`::

        abjad> staff = Staff("c' d' e' f'")
    
    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    ::

        abjad> staff[1]
        Note("d'4")

    Return sibling to the right of `component` for positive `n`::

        abjad> componenttools.get_nth_sibling_from_component(staff[1], 1)
        Note("e'4")

    Return sibling to the left of `component` for negative `n`::

        abjad> componenttools.get_nth_sibling_from_component(staff[1], -1)
        Note("c'4")

    Return `component` when `n` is ``0``::

        abjad> componenttools.get_nth_sibling_from_component(staff[1], 0)
        Note("d'4")

    Return none when `n` is out of range::

        abjad> componenttools.get_nth_sibling_from_component(staff[1], 99) is None
        True

    Return none when `component` has no parent::

        abjad> componenttools.get_nth_sibling_from_component(staff, 1) is None
        True

    Return component or none.
    '''

    if n == 0:
        return component
    elif 0 < n:
        if component.parent is not None:
            if not component.parent.is_parallel:    
                index = component.parent.index(component)
                if index + n < len(component.parent):
                    return component.parent[index + n]
    elif n < 0:
        if component.parent is not None:
            if not component.parent.is_parallel:
                index = component.parent.index(component)
                if 0 <= index + n:
                    return component.parent[index + n]
