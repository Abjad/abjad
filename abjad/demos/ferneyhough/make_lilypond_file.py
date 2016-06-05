# -*- coding: utf-8 -*-
import abjad
from abjad.tools import lilypondfiletools


def make_lilypond_file(tuplet_duration, row_count, column_count):
    r'''Makes LilyPond file.
    '''

    score = abjad.demos.ferneyhough.make_score(
        tuplet_duration,
        row_count,
        column_count,
        )
    abjad.demos.ferneyhough.configure_score(score)
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    abjad.demos.ferneyhough.configure_lilypond_file(lilypond_file)
    return lilypond_file