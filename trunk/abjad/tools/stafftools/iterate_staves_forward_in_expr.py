from abjad.tools.stafftools.Staff import Staff
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr


def iterate_staves_forward_in_expr(expr, start = 0, stop = None):
    r'''.. versionadded:: 2.0

    Iterate staves forward in `expr`::

        abjad> score = Score(4 * Staff([]))

    ::

        abjad> f(score)
        \new Score <<
            \new Staff {
            }
            \new Staff {
            }
            \new Staff {
            }
            \new Staff {
            }
        >>

    ::

        abjad> for staff in stafftools.iterate_staves_forward_in_expr(score):
        ...     staff
        ...
        Staff{}
        Staff{}
        Staff{}
        Staff{}

    Return generator.
    '''

    return iterate_components_forward_in_expr(expr, Staff, start = start, stop = stop)
