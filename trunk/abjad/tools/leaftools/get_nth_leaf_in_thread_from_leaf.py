from abjad.tools.leaftools._Leaf import _Leaf


def get_nth_leaf_in_thread_from_leaf(leaf, n = 0):
    r'''.. versionadded:: 2.0

    Get `n` th leaf in thread from `leaf`::

        abjad> staff = Staff(2 * Voice("c'8 d'8 e'8 f'8"))
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> f(staff)
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

        abjad> for n in range(8):
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

    if not isinstance(leaf, _Leaf):
        return None

    current_leaf = leaf

    if n < 0:
        for i in range(abs(n)):
            current_leaf = current_leaf._navigator._prev_bead
            if current_leaf is None:
                break
    elif n == 0:
        pass
    else:
        for i in range(n):
            current_leaf = current_leaf._navigator._next_bead
            if current_leaf is None:
                break

    return current_leaf
