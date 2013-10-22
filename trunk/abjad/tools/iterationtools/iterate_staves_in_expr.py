# -*- encoding: utf-8 -*-
from abjad.tools import stafftools


def iterate_staves_in_expr(expr, reverse=False, start=0, stop=None):
    r'''Iterate staves forward in `expr`:

    ::

        >>> score = Score(4 * Staff([]))

    ..  doctest::

        >>> f(score)
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

        >>> for staff in iterationtools.iterate_staves_in_expr(score):
        ...     staff
        ...
        Staff{}
        Staff{}
        Staff{}
        Staff{}

    Iterate staves backward in `expr`:

    ::

    ::

        >>> for staff in iterationtools.iterate_staves_in_expr(score, reverse=True):
        ...     staff
        ...
        Staff{}
        Staff{}
        Staff{}
        Staff{}

    Returns generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr,
        component_class=stafftools.Staff,
        reverse=reverse,
        start=start,
        stop=stop,
        )
