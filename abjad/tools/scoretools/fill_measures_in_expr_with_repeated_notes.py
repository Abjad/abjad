# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.topleveltools import iterate


def fill_measures_in_expr_with_repeated_notes(
    expr, written_duration, iterctrl=None):
    '''Fill measures in `expr` with repeated notes.
    '''
    from abjad.tools import scoretools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    written_duration = durationtools.Duration(written_duration)
    for i, measure in enumerate(iterate(expr).by_class(scoretools.Measure)):
        if iterctrl(measure, i):
            time_signature = measure.time_signature
            total_duration = time_signature.duration
            prolation = time_signature.implied_prolation
            notes = scoretools.make_repeated_notes_with_shorter_notes_at_end(
                0, written_duration, total_duration, prolation)
            measure[:] = notes
