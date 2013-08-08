# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import notetools
from abjad.tools.selectiontools import more


def fill_measures_in_expr_with_repeated_notes(expr, written_duration, iterctrl=None):
    '''Fill measures in `expr` with repeated notes.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools

    if iterctrl is None:
        iterctrl = lambda measure, i: True
    written_duration = durationtools.Duration(written_duration)
    for i, measure in enumerate(iterationtools.iterate_measures_in_expr(expr)):
        if iterctrl(measure, i):
            time_signature = more(measure).get_effective_context_mark(
                contexttools.TimeSignatureMark)
            total_duration = time_signature.duration
            prolation = time_signature.implied_prolation
            notes = notetools.make_repeated_notes_with_shorter_notes_at_end(
                0, written_duration, total_duration, prolation)
            measure[:] = notes
