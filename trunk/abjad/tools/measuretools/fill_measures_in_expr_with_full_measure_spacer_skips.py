# -*- encoding: utf-8 -*-
from abjad.tools import skiptools


def fill_measures_in_expr_with_full_measure_spacer_skips(expr, iterctrl=None):
    '''.. versionadded:: 1.1

    Fill measures in `expr` with full-measure spacer skips.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools

    if iterctrl is None:
        iterctrl = lambda measure, i: True

    for i, measure in enumerate(iterationtools.iterate_measures_in_expr(expr)):
        if iterctrl(measure, i):
            skip = skiptools.Skip(1)
            # allow zero-update iteration
            time_signature = measure.get_effective_context_mark(
                contexttools.TimeSignatureMark)
            skip.duration_multiplier = \
                time_signature.duration / time_signature.implied_prolation
            measure[:] = [skip]
            for spanner in measure.spanners:
                spanner._remove(component)
