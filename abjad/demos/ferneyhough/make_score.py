# -*- coding: utf-8 -*-
import abjad
from abjad.demos import ferneyhough


def make_score(tuplet_duration, row_count, column_count):
    r'''Makes score.
    '''

    score = abjad.Score()
    rows_of_nested_tuplets = ferneyhough.make_rows_of_nested_tuplets(
        tuplet_duration,
        row_count,
        column_count,
        )
    for row_of_nested_tuplets in rows_of_nested_tuplets:
        staff = abjad.Staff(row_of_nested_tuplets)
        staff.context_name = 'RhythmicStaff'
        time_signature = abjad.TimeSignature((1, 4))
        abjad.attach(time_signature, staff)
        score.append(staff)
    return score
