from abjad import *
from abjad.demos.ferneyhough.make_rows_of_nested_tuplets import make_rows_of_nested_tuplets
from abjad.demos.ferneyhough.configure_score import configure_score
from abjad.demos.ferneyhough.configure_lilypond_file import configure_lilypond_file


def make_lilypond_file(tuplet_duration, row_count, column_count):
    rows_of_nested_tuplets = make_rows_of_nested_tuplets(tuplet_duration, row_count, column_count)
    all_nested_tuplets = sequencetools.flatten_sequence(rows_of_nested_tuplets)
    staff = stafftools.RhythmicStaff(all_nested_tuplets)
    time_signature  = contexttools.TimeSignatureMark((1, 4))
    time_signature.attach(staff)
    score = Score([staff])
    configure_score(score)
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    configure_lilypond_file(lilypond_file)
    return lilypond_file

