from abjad.tools import componenttools


def get_nth_leaf_in_thread_from_leaf(leaf, n=0):
    r'''.. versionadded:: 2.0

    Get `n` th leaf in thread from `leaf`::

        >>> staff = Staff(2 * Voice("c'8 d'8 e'8 f'8"))
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ::

        >>> f(staff)
        \new Staff {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
                b'8
                c''8
            }
        }

    ::

        >>> for n in range(8):
        ...     print n, leaftools.get_nth_leaf_in_thread_from_leaf(staff[0][0], n)
        ...
        0 c'8
        1 d'8
        2 e'8
        3 f'8
        4 None
        5 None
        6 None
        7 None

    Return leaf or none.
    '''
    from abjad.tools import leaftools

    if not isinstance(leaf, leaftools.Leaf):
        return None

    def _next(component):
        new_component = componenttools.get_nth_component_in_time_order_from_component(component, 1)
        if new_component is None:
            return
        candidates = componenttools.get_improper_descendents_of_component_that_start_with_component(
            new_component)
        candidates = [x for x in candidates if isinstance(x, leaftools.Leaf)]
        for candidate in candidates:
            if componenttools.all_are_components_in_same_thread([component, candidate]):
                return candidate

    def _prev(component):
        new_component = componenttools.get_nth_component_in_time_order_from_component(component, -1)
        if new_component is None:
            return
        candidates = componenttools.get_improper_descendents_of_component_that_stop_with_component(
            new_component)
        candidates = [x for x in candidates if isinstance(x, leaftools.Leaf)]
        for candidate in candidates:
            if componenttools.all_are_components_in_same_thread([component, candidate]):
                return candidate

    current_leaf = leaf

    if n < 0:
        for i in range(abs(n)):
            current_leaf = _prev(current_leaf)
            if current_leaf is None:
                break
    elif n == 0:
        pass
    else:
        for i in range(n):
            current_leaf = _next(current_leaf)
            if current_leaf is None:
                break

    return current_leaf
