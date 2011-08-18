from abjad import *


def test_chordtools_iterate_chords_backward_in_expr_01():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    chords = chordtools.iterate_chords_backward_in_expr(staff)
    chords = list(chords)

    assert chords[0] is staff[3]
    assert chords[1] is staff[0]
