# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_pitch_classs_number_01():

    assert pitchtools.NamedPitch("cs''").pitch_class_number == 1
