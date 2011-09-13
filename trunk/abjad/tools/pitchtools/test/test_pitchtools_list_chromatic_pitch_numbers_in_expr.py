from abjad import *


def test_pitchtools_list_chromatic_pitch_numbers_in_expr_01():

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert pitchtools.list_chromatic_pitch_numbers_in_expr(t) == (0, 2, 4)


def test_pitchtools_list_chromatic_pitch_numbers_in_expr_02():

    t = Staff("c'8 d'8 e'8 f'8")
    assert pitchtools.list_chromatic_pitch_numbers_in_expr(t) == (0, 2, 4, 5)
