# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_transpose_pitch_class_number_to_pitch_number_neighbor_01():

    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 0) == 12
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 1) == 13
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 2) == 14
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 3) == 15
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 4) == 16
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 5) == 17


def test_pitchtools_transpose_pitch_class_number_to_pitch_number_neighbor_02():

    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 6) == 6
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 7) == 7
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 8) == 8
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 9) == 9
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 10) == 10
    assert pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(12, 11) == 11
