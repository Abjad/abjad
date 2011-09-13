from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr


def fill_measures_in_expr_with_little_endian_notes(expr, iterctrl = None):
    '''.. versionadded:: 1.1

    Fill measures in `expr` with little-endian notes.
    '''
    from abjad.tools import contexttools
    from abjad.tools import notetools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    for i, measure in enumerate(iterate_measures_forward_in_expr(expr)):
        if iterctrl(measure, i):
            meter = contexttools.get_effective_time_signature(measure)
            written_duration = meter.duration / meter.multiplier
            notes = notetools.make_notes(0, written_duration, direction = 'little-endian')
            measure[:] = notes
