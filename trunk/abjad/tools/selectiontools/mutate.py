# -*- encoding: utf-8 -*-


def mutate(expr):
    r'''Wraps `expr` in a contiguous selection for subsequent mutation.

    Returns contiguous selection.
    '''
    from abjad.tools import selectiontools
    return selectiontools.ContiguousSelection(music=expr)
