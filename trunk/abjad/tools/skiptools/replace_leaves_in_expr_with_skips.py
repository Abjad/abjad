from abjad.tools import componenttools


def replace_leaves_in_expr_with_skips(expr):
    r'''.. versionadded:: 1.1

    Replace leaves in `expr` with skips::

        >>> staff = Staff(Measure((2, 8), "c'8 d'8") * 2)
        >>> skiptools.replace_leaves_in_expr_with_skips(staff[0])

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                s8
                s8
            }
            {
                c'8
                d'8
            }
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``leaftools.replace_leaves_with_skips_in()`` to
        ``skiptools.replace_leaves_in_expr_with_skips()``.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import skiptools

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        skip = skiptools.Skip(leaf)
        componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [skip])
