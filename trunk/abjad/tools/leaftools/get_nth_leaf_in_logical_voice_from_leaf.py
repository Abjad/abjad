# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def get_nth_leaf_in_logical_voice_from_leaf(leaf, n=0):
    r'''Gets `n` th leaf in logical voice from `leaf`.

    ::

        >>> staff = Staff(2 * Voice("c'8 d'8 e'8 f'8"))
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        ...     staff)

    ..  doctest::

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
        ...     print n, leaftools.get_nth_leaf_in_logical_voice_from_leaf(
        ...     staff[0][0], n)
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
    from abjad.tools import selectiontools
    Selection = selectiontools.Selection

    if not isinstance(leaf, leaftools.Leaf):
        return None

    def next(component):
        new_component = component._get_nth_component_in_time_order_from(1)
        if new_component is None:
            return
        candidates = new_component._get_descendants_starting_with()
        candidates = [x for x in candidates if isinstance(x, leaftools.Leaf)]
        for candidate in candidates:
            if Selection._all_are_components_in_same_logical_voice(
                [component, candidate]):
                return candidate

    def previous(component):
        new_component = component._get_nth_component_in_time_order_from(-1)
        if new_component is None:
            return
        candidates = new_component._get_descendants_stopping_with()
        candidates = [x for x in candidates if isinstance(x, leaftools.Leaf)]
        for candidate in candidates:
            if Selection._all_are_components_in_same_logical_voice(
                [component, candidate]):
                return candidate

    current_leaf = leaf

    if n < 0:
        for i in range(abs(n)):
            current_leaf = previous(current_leaf)
            if current_leaf is None:
                break
    elif n == 0:
        pass
    else:
        for i in range(n):
            current_leaf = next(current_leaf)
            if current_leaf is None:
                break

    return current_leaf
