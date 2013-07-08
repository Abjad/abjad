from abjad.tools import componenttools
from abjad.tools import iterationtools


def _withdraw_components_in_expr_from_attached_spanners(expr):
    '''Find every spanner in `expr`.
    Withdraw all components in `expr` from spanners.
    Return `expr`.
    Not composer-safe.
    '''

    # check input
    assert componenttools.all_are_thread_contiguous_components(expr)

    # withdraw components from attached spanners
    for component in iterationtools.iterate_components_in_expr(expr):
        for spanner in component.spanners:
            spanner._remove(component)

    # return expr
    return expr
