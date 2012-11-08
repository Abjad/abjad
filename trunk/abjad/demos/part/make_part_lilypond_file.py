from abjad import *
from abjad.demos.part.PartCantusScoreTemplate import PartCantusScoreTemplate
from abjad.demos.part.add_bell_music_to_score import add_bell_music_to_score
from abjad.demos.part.add_string_music_to_score import add_string_music_to_score
from abjad.demos.part.apply_bowing_marks import apply_bowing_marks
from abjad.demos.part.apply_dynamic_marks import apply_dynamic_marks
from abjad.demos.part.apply_expressive_marks import apply_expressive_marks
from abjad.demos.part.apply_page_breaks import apply_page_breaks
from abjad.demos.part.apply_rehearsal_marks import apply_rehearsal_marks
from abjad.demos.part.configure_lilypond_file import configure_lilypond_file
from abjad.demos.part.configure_score import configure_score


def make_part_lilypond_file():

    score_template = PartCantusScoreTemplate()
    score = score_template()

    add_bell_music_to_score(score)
    add_string_music_to_score(score)

    apply_bowing_marks(score)
    apply_dynamic_marks(score)
    apply_expressive_marks(score)
    apply_page_breaks(score)
    apply_rehearsal_marks(score)

    configure_score(score)
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    configure_lilypond_file(lilypond_file)

    return lilypond_file
