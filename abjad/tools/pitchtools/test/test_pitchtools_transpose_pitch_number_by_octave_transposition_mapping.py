# -*- coding: utf-8 -*-
from abjad import *


function = pitchtools.transpose_pitch_number_by_octave_transposition_mapping


def test_pitchtools_transpose_pitch_number_by_octave_transposition_mapping_01():

    mapping = [((-39, -13), 0), ((-12, 23), 12), ((24, 48), 24)]
    pitch_numbers = [-30, -18, -6, 6, 18, 30, 42]

    new_pitch_numbers = []
    for pitch_number in pitch_numbers:
        new_pitch_numbers.append(function(pitch_number, mapping))

    assert new_pitch_numbers == [6, 6, 18, 18, 18, 30, 30]

    # NEW WAY:
    components = [('(-39, -13)', 0), ('(-12, 23)', 12), ('(24, 48)', 24)]
    registration = pitchtools.Registration(components)
    pitch_numbers = [-30, -18, -6, 6, 18, 30, 42]
    new_pitch_numbers = registration(pitch_numbers)

    assert new_pitch_numbers == [6, 6, 18, 18, 18, 30, 30]


def test_pitchtools_transpose_pitch_number_by_octave_transposition_mapping_02():

    mapping = [((-39, -1), 0), ((0, 48), 6)]
    pitch_numbers = [-30, -18, -6, 6, 18, 30, 42]

    new_pitch_numbers = []
    for pitch_number in pitch_numbers:
        new_pitch_numbers.append(function(pitch_number, mapping))

    assert new_pitch_numbers == [6, 6, 6, 6, 6, 6, 6]


def test_pitchtools_transpose_pitch_number_by_octave_transposition_mapping_03():

    mapping = [((-39, -1), 0), ((0, 48), 6)]
    pitch_numbers = [-34, -22, -10, 2, 14, 26, 38]

    new_pitch_numbers = []
    for pitch_number in pitch_numbers:
        new_pitch_numbers.append(function(pitch_number, mapping))

    assert new_pitch_numbers == [2, 2, 2, 14, 14, 14, 14]
