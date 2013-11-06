# -*- encoding: utf-8 -*-


def iterate_components_in_expr(
    expr,
    component_class=None,
    reverse=False,
    start=0,
    stop=None,
    ):
    r'''Iterate components forward in `expr`.
    '''
    from abjad.tools import functiontools
    return functiontools.iterate(expr).by_class(
        component_classes=component_class,
        reverse=reverse,
        start=start,
        stop=stop,
        )
