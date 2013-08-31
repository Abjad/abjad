# -*- encoding: utf-8 -*-


def scale_contents_of_measures_in_expr(expr, multiplier=1):
    '''Scale contents of measures in `expr` by `multiplier`.

    Iterate expr. For every measure in expr first multiply the measure
    time siganture by `multiplier` and then scale measure contents to fit
    the new time signature.

    Extend ``containertools.scale_contents_of_container()``.

    Return none.
    '''
    from abjad.tools import iterationtools

    for measure in iterationtools.iterate_measures_in_expr(expr):
        measure.scale(multiplier)
