# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_pitch_class_octave_label_01():

    named_pitch = pitchtools.NamedPitch("cs''")
    assert named_pitch.pitch_class_octave_label == 'C#5'
