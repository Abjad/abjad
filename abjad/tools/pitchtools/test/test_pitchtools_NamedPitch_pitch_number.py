# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch_pitch_number_01():

    assert NamedPitch("cs''").pitch_number == 13
