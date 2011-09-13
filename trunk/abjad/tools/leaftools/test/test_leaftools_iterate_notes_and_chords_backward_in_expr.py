from abjad import *


def test_leaftools_iterate_notes_and_chords_backward_in_expr_01():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    notes_and_chords = leaftools.iterate_notes_and_chords_backward_in_expr(staff)
    notes_and_chords = list(notes_and_chords)

    assert len(notes_and_chords) == 3
    assert notes_and_chords[0] is staff[3]
    assert notes_and_chords[1] is staff[1]
    assert notes_and_chords[2] is staff[0]
