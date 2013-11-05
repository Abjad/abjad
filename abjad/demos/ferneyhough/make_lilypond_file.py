# -*- encoding: utf-8 -*-
from abjad import *
from abjad.demos.ferneyhough.configure_score import configure_score
from abjad.demos.ferneyhough.configure_lilypond_file import configure_lilypond_file
from abjad.demos.ferneyhough.make_score import make_score


def make_lilypond_file(tuplet_duration, row_count, column_count):
    score = make_score(tuplet_duration, row_count, column_count)
    configure_score(score)
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    configure_lilypond_file(lilypond_file)
    return lilypond_file
