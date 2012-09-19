from abjad import *


def test_iterationtools_iterate_chords_in_expr_01():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    chords = iterationtools.iterate_chords_in_expr(staff)
    chords = list(chords)

    assert chords[0] is staff[0]
    assert chords[1] is staff[3]

def test_iterationtools_iterate_chords_in_expr_02():

    staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    chords = iterationtools.iterate_chords_in_expr(staff, reverse=True)
    chords = list(chords)

    assert chords[0] is staff[3]
    assert chords[1] is staff[0]
