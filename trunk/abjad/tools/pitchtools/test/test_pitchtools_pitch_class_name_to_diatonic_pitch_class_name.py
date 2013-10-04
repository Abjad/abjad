# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_pitch_class_name_to_diatonic_pitch_class_name_01():

    assert pitchtools.pitch_class_name_to_diatonic_pitch_class_name('c') == 'c'
    assert pitchtools.pitch_class_name_to_diatonic_pitch_class_name('cs') == 'c'
    assert pitchtools.pitch_class_name_to_diatonic_pitch_class_name('cf') == 'c'
    assert pitchtools.pitch_class_name_to_diatonic_pitch_class_name('cqs') == 'c'
    assert pitchtools.pitch_class_name_to_diatonic_pitch_class_name('cqf') == 'c'
