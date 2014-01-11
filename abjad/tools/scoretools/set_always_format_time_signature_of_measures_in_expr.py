# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import iterate


def set_always_format_time_signature_of_measures_in_expr(expr, value=True):
    '''Set `always_format_time_signature` of measures in `expr` to 
    boolean `value`.

    Returns none.
    '''
    from abjad.tools import scoretools
    for measure in iterate(expr).by_class(scoretools.Measure):
        measure.always_format_time_signature = value
