# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Octave_from_pitch_name_01():

    assert pitchtools.Octave.from_pitch_name("cs'") == 4
    assert pitchtools.Octave.from_pitch_name('cs') == 3
    assert pitchtools.Octave.from_pitch_name('cs,') == 2
