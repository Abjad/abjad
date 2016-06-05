# -*- coding: utf-8 -*-
import abjad
from abjad.tools import lilypondfiletools


def make_part_lilypond_file():
    r'''Makes Pärt LilyPond file.
    '''
    score_template = abjad.demos.part.PartCantusScoreTemplate()
    score = score_template()
    abjad.demos.part.add_bell_music_to_score(score)
    abjad.demos.part.add_string_music_to_score(score)
    abjad.demos.part.apply_bowing_marks(score)
    abjad.demos.part.apply_dynamics(score)
    abjad.demos.part.apply_expressive_marks(score)
    abjad.demos.part.apply_page_breaks(score)
    abjad.demos.part.apply_rehearsal_marks(score)
    abjad.demos.part.apply_final_bar_lines(score)
    abjad.demos.part.configure_score(score)
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    abjad.demos.part.configure_lilypond_file(lilypond_file)
    return lilypond_file