# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_chomatic_pitch_number_01():

    assert pitchtools.NamedPitch("cs''").pitch_number == 13
