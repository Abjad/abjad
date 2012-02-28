from abjad.tools.resttools.Rest import Rest


def replace_leaves_in_expr_with_rests(expr):
    r'''.. versionadded:: 1.1

    Replace leaves in `expr` with rests::

        abjad> staff = Staff(Measure((2, 8), "c'8 d'8") * 2)
        abjad> resttools.replace_leaves_in_expr_with_rests(staff[0])
        abjad> print staff.format
        \new Staff {
            {
                \time 2/8
                r8
                r8
            }
            {
                \time 2/8
                c'8
                d'8
            }
        }

    Return none.
    '''
    from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr
    from abjad.tools import componenttools

    for leaf in iterate_leaves_forward_in_expr(expr):
        rest = Rest(leaf)
        componenttools.move_parentage_and_spanners_from_components_to_components([leaf], [rest])
