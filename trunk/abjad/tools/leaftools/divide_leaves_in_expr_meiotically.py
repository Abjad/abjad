from abjad.tools import componenttools


def divide_leaves_in_expr_meiotically(expr, n=2):
    r'''.. versionadded:: 1.1

    Divide leaves meiotically in `expr` `n` times::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)
        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> leaftools.divide_leaves_in_expr_meiotically(staff[2:], n=4)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'32
            e'32
            e'32
            e'32
            f'32
            f'32
            f'32
            f'32 ]
        }

    Replace every leaf in `expr` with `n` new leaves.

    Preserve parentage and spanners.

    Allow divisions into only ``1, 2, 4, 8, 16, ...`` and other
    nonnegative integer powers of ``2``.

    Produce only leaves and never tuplets or other containers.

    Return none.

    .. versionchanged:: 2.0
        renamed ``leaftools.meiose()`` to
        ``leaftools.divide_leaves_in_expr_meiotically()``.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import leaftools

    # can not wrap with update control because ofextend_in_parent_of_component()
    for leaf in iterationtools.iterate_leaves_in_expr(expr, reverse=True):
        leaftools.divide_leaf_meiotically(leaf, n)
