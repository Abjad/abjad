# -*- coding: utf-8 -*-
import abjad
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach


def make_score(tuplet_duration, row_count, column_count):
    r'''Makes score.
    '''

    score = scoretools.Score()
    rows_of_nested_tuplets = \
        abjad.demos.ferneyhough.make_rows_of_nested_tuplets(
        tuplet_duration, row_count, column_count)
    for row_of_nested_tuplets in rows_of_nested_tuplets:
        staff = scoretools.Staff(row_of_nested_tuplets)
        staff.context_name = 'RhythmicStaff'
        time_signature = indicatortools.TimeSignature((1, 4))
        attach(time_signature, staff)
        score.append(staff)
    return score