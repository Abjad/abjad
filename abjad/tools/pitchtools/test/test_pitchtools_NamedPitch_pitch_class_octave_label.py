# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch_pitch_class_octave_label_01():

    named_pitch = NamedPitch("cs''")
    assert named_pitch.pitch_class_octave_label == 'C#5'
