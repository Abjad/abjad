# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_RegistrationComponent_source_pitch_range_01():

    component = pitchtools.RegistrationComponent('[A0, C8]', 15)
    assert component.source_pitch_range == pitchtools.PitchRange('[A0, C8]')
