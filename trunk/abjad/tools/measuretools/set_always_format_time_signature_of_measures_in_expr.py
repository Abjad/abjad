def set_always_format_time_signature_of_measures_in_expr(expr, value=True):
    '''.. versionadded:: 2.9

    Set `always_format_time_signature` of measures in `expr` to boolean `value`.

    Return none.
    '''
    from abjad.tools import iterationtools

    for measure in iterationtools.iterate_measures_in_expr(expr):
        measure.always_format_time_signature = value
