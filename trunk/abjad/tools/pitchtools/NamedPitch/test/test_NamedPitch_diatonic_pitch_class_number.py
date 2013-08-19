# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_diatonic_pitch_class_number_01():

    assert pitchtools.NamedPitch("cs''").diatonic_pitch_class_number == 0
