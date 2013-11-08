# -*- encoding: utf-8 -*-
from abjad import *


def test_ClefMark_middle_c_position_01():

    assert ClefMark('treble').middle_c_position == -6
    assert ClefMark('alto').middle_c_position == 0
    assert ClefMark('tenor').middle_c_position == 2
    assert ClefMark('bass').middle_c_position == 6
    assert ClefMark('treble^8').middle_c_position == -13
    assert ClefMark('alto^15').middle_c_position == -13
    assert ClefMark('tenor_8').middle_c_position == 9
    assert ClefMark('bass_15').middle_c_position == 19
