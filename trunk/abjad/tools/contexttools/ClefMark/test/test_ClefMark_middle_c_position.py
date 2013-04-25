from abjad import *


def test_ClefMark_middle_c_position_01():

    assert contexttools.ClefMark('treble').middle_c_position == -6
    assert contexttools.ClefMark('alto').middle_c_position == 0
    assert contexttools.ClefMark('tenor').middle_c_position == 2
    assert contexttools.ClefMark('bass').middle_c_position == 6
    assert contexttools.ClefMark('treble^8').middle_c_position == -13
    assert contexttools.ClefMark('alto^15').middle_c_position == -13
    assert contexttools.ClefMark('tenor_8').middle_c_position == 9
    assert contexttools.ClefMark('bass_15').middle_c_position == 19
