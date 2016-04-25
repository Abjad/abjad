# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_RegistrationComponent_target_octave_start_pitch_01():

    component = pitchtools.RegistrationComponent('[A0, C8]', 15)
    assert component.target_octave_start_pitch == pitchtools.NumberedPitch(15)
