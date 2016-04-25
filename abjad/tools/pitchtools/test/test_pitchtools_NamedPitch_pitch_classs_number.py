# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch_pitch_classs_number_01():

    assert NamedPitch("cs''").pitch_class_number == 1
