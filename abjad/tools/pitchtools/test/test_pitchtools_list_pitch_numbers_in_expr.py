# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_list_pitch_numbers_in_expr_01():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert pitchtools.list_pitch_numbers_in_expr(tuplet) == (0, 2, 4)


def test_pitchtools_list_pitch_numbers_in_expr_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    assert pitchtools.list_pitch_numbers_in_expr(staff) == (0, 2, 4, 5)
