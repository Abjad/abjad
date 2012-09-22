from abjad import *


def test_iterationtools_iterate_notes_and_chords_in_expr_01():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    notes_and_chords = iterationtools.iterate_notes_and_chords_in_expr(staff, reverse=True)
    notes_and_chords = list(notes_and_chords)

    assert len(notes_and_chords) == 3
    assert notes_and_chords[0] is staff[3]
    assert notes_and_chords[1] is staff[1]
    assert notes_and_chords[2] is staff[0]

def test_iterationtools_iterate_notes_and_chords_in_expr_02():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    notes_and_chords = iterationtools.iterate_notes_and_chords_in_expr(staff)
    notes_and_chords = list(notes_and_chords)

    assert len(notes_and_chords) == 3
    assert notes_and_chords[0] is staff[0]
    assert notes_and_chords[1] is staff[1]
    assert notes_and_chords[2] is staff[3]
