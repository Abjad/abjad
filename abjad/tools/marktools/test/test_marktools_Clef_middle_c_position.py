# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Clef_middle_c_position_01():

    assert Clef('treble').middle_c_position == -6
    assert Clef('alto').middle_c_position == 0
    assert Clef('tenor').middle_c_position == 2
    assert Clef('bass').middle_c_position == 6
    assert Clef('treble^8').middle_c_position == -13
    assert Clef('alto^15').middle_c_position == -13
    assert Clef('tenor_8').middle_c_position == 9
    assert Clef('bass_15').middle_c_position == 19
