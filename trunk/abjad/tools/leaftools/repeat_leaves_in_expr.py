def repeat_leaves_in_expr(expr, total=1):
    r'''.. versionadded:: 1.1

    Repeat leaves in `expr` and extend spanners::

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

        >>> result = leaftools.repeat_leaves_in_expr(staff[2:], total=3)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            e'8
            e'8
            f'8
            f'8
            f'8 ]
        }

    Preserve leaf written durations.

    Preserve parentage and spanners.

    Return none.

    .. versionchanged:: 2.0
        renamed ``leaftools.multiply()`` to
        ``leaftools.repeat_leaves_in_expr()``.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import leaftools

    for leaf in iterationtools.iterate_leaves_in_expr(expr, reverse=True):
        leaftools.repeat_leaf(leaf, total)
