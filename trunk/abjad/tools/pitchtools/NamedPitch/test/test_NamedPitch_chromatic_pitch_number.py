# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_chromatic_pitch_number_01():

    assert pitchtools.NamedPitch("cs''").chromatic_pitch_number == 13
