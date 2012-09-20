from abjad.tools import componenttools


def replace_leaves_in_expr_with_rests(expr):
    r'''.. versionadded:: 1.1

    Replace leaves in `expr` with rests::

        >>> staff = Staff(Measure((2, 8), "c'8 d'8") * 2)
        >>> resttools.replace_leaves_in_expr_with_rests(staff[0])

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                r8
                r8
            }
            {
                c'8
                d'8
            }
        }

    Return none.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import resttools

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        rest = resttools.Rest(leaf)
        componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [rest])
