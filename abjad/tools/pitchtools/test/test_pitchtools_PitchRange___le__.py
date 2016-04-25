# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___le___01():

    pitch_range = pitchtools.PitchRange.from_pitches(-39, 48)

    assert not pitch_range <= -99
    assert not pitch_range <= -39
    assert not pitch_range <= 0
    assert pitch_range <= 48
    assert pitch_range <= 99


def test_pitchtools_PitchRange___le___02():

    pitch_range = pitchtools.PitchRange.from_pitches(-39, 48)

    assert not pitch_range <= NamedPitch(-99)
    assert not pitch_range <= NamedPitch(-39)
    assert not pitch_range <= NamedPitch(0)
    assert pitch_range <= NamedPitch(48)
    assert pitch_range <= NamedPitch(99)
