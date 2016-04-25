# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Octave_from_pitch_number_01():

    assert pitchtools.Octave.from_pitch_number(-12) == 3
    assert pitchtools.Octave.from_pitch_number(-11) == 3
    assert pitchtools.Octave.from_pitch_number(0) == 4
    assert pitchtools.Octave.from_pitch_number(1) == 4
    assert pitchtools.Octave.from_pitch_number(12) == 5
    assert pitchtools.Octave.from_pitch_number(13) == 5
