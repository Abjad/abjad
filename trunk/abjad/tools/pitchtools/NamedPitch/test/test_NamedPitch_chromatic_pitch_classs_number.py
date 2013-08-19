# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_chromatic_pitch_classs_number_01():

    assert pitchtools.NamedPitch("cs''").chromatic_pitch_class_number == 1
