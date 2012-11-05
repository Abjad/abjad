from abjad.demos.part.PartCantusScoreTemplate import PartCantusScoreTemplate
from abjad.demos.part.add_bell_music_to_score import add_bell_music_to_score
from abjad.demos.part.add_string_music_to_score import add_string_music_to_score
from abjad.demos.part.apply_dynamic_marks import apply_dynamic_marks
from abjad.demos.part.apply_expressive_marks import apply_expressive_marks
from abjad.demos.part.apply_page_breaks import apply_page_breaks
from abjad.demos.part.apply_rehearsal_marks import apply_rehearsal_marks
from abjad.demos.part.format_lilypond_file import format_lilypond_file


def build_score():

    score_template = PartCantusScoreTemplate()
    score = score_template()

    add_bell_music_to_score(score)
    add_string_music_to_score(score)

    apply_dynamic_marks(score)
    apply_expressive_marks(score)
    apply_page_breaks(score)
    apply_rehearsal_marks(score)

    lilypond_file = format_lilypond_file(score)

    return lilypond_file
