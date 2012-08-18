from abjad.tools import contexttools


def fill_measures_in_expr_with_big_endian_notes(expr, iterctrl=None):
    '''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``measuretools.fill_measures_in_expr_with_minimal_number_of_notes()`` instead.

    Fill measures in `expr` with big-endian notes.
    '''
    from abjad.tools import measuretools
    from abjad.tools import notetools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    for i, measure in enumerate(measuretools.iterate_measures_forward_in_expr(expr)):
        if iterctrl(measure, i):
            meter = contexttools.get_effective_time_signature(measure)
            written_duration = meter.duration / meter.multiplier
            notes = notetools.make_notes(0, written_duration)
            measure[:] = notes
