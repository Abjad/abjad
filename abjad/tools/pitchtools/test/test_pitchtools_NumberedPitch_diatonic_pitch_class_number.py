# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch_diatonic_pitch_class_number_01():

    assert pitchtools.NumberedPitch(11).diatonic_pitch_class_number == 6
    assert pitchtools.NumberedPitch(12).diatonic_pitch_class_number == 0
    assert pitchtools.NumberedPitch(13).diatonic_pitch_class_number == 0
    assert pitchtools.NumberedPitch(14).diatonic_pitch_class_number == 1
    assert pitchtools.NumberedPitch(15).diatonic_pitch_class_number == 2


def test_pitchtools_NumberedPitch_diatonic_pitch_class_number_02():

    assert pitchtools.NumberedPitch(11).diatonic_pitch_class_number == 6
    assert pitchtools.NumberedPitch(12).diatonic_pitch_class_number == 0
    assert pitchtools.NumberedPitch(13).diatonic_pitch_class_number == 0
    assert pitchtools.NumberedPitch(14).diatonic_pitch_class_number == 1
