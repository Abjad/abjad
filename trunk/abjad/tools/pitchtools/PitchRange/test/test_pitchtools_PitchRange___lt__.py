# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___lt___01():

    pitch_range = pitchtools.PitchRange(-39, 48)

    assert not pitch_range < -99
    assert not pitch_range < -39
    assert not pitch_range < 0
    assert not pitch_range < 48
    assert pitch_range < 99


def test_pitchtools_PitchRange___lt___02():

    pitch_range = pitchtools.PitchRange(-39, 48)

    assert not pitch_range < pitchtools.NamedPitch(-99)
    assert not pitch_range < pitchtools.NamedPitch(-39)
    assert not pitch_range < pitchtools.NamedPitch(0)
    assert not pitch_range < pitchtools.NamedPitch(48)
    assert pitch_range < pitchtools.NamedPitch(99)
