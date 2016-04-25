# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitchClass_diatonic_pitch_class_number_01():

    assert pitchtools.NumberedPitchClass(0).diatonic_pitch_class_number == 0
    assert pitchtools.NumberedPitchClass(1).diatonic_pitch_class_number == 0
    assert pitchtools.NumberedPitchClass(2).diatonic_pitch_class_number == 1
    assert pitchtools.NumberedPitchClass(3).diatonic_pitch_class_number == 2
    assert pitchtools.NumberedPitchClass(4).diatonic_pitch_class_number == 2
    assert pitchtools.NumberedPitchClass(5).diatonic_pitch_class_number == 3
    assert pitchtools.NumberedPitchClass(6).diatonic_pitch_class_number == 3
    assert pitchtools.NumberedPitchClass(7).diatonic_pitch_class_number == 4
    assert pitchtools.NumberedPitchClass(8).diatonic_pitch_class_number == 5
    assert pitchtools.NumberedPitchClass(9).diatonic_pitch_class_number == 5
    assert pitchtools.NumberedPitchClass(10).diatonic_pitch_class_number == 6
    assert pitchtools.NumberedPitchClass(11).diatonic_pitch_class_number == 6
