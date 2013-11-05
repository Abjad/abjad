# -*- encoding: utf-8 -*-
from abjad import *
from abjad.demos.ferneyhough.make_rows_of_nested_tuplets import make_rows_of_nested_tuplets


def make_score(tuplet_duration, row_count, column_count):
    score = Score()
    rows_of_nested_tuplets = make_rows_of_nested_tuplets(
        tuplet_duration, row_count, column_count)
    for row_of_nested_tuplets in rows_of_nested_tuplets:
        staff = scoretools.RhythmicStaff(row_of_nested_tuplets)
        time_signature = marktools.TimeSignatureMark((1, 4))
        attach(time_signature, staff)
        score.append(staff)
    return score
