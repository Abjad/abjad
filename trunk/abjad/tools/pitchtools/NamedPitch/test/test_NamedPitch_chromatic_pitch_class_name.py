# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_pitch_class_name_01():

    assert pitchtools.NamedPitch("cs''").chromatic_pitch_class_number == 1
