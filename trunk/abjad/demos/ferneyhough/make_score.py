# -*- encoding: utf-8 -*-
from abjad import *
from abjad.demos.ferneyhough.make_rows_of_nested_tuplets import make_rows_of_nested_tuplets


def make_score(tuplet_duration, row_count, column_count):
    rows_of_nested_tuplets = make_rows_of_nested_tuplets(tuplet_duration, row_count, column_count)
    all_nested_tuplets = sequencetools.flatten_sequence(rows_of_nested_tuplets)
    staff = stafftools.RhythmicStaff(all_nested_tuplets)
    time_signature = contexttools.TimeSignatureMark((1, 4))
    time_signature.attach(staff)
    score = Score([staff])
    return score
