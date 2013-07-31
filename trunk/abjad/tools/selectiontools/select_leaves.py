# -*- encoding: utf-8 -*-
def select_leaves(expr=None):
    from abjad.tools import iterationtools
    from abjad.tools import selectiontools
    expr = iterationtools.iterate_leaves_in_expr(expr)
    selection = selectiontools.LeafSelection(music=expr)
    return selection

