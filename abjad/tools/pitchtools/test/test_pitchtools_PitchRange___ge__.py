# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___ge___01():

    pitch_range = pitchtools.PitchRange.from_pitches(-39, 48)

    assert -99 <= pitch_range
    assert -39 <= pitch_range
    assert not 0 <= pitch_range
    assert not 48 <= pitch_range
    assert not 99 <= pitch_range


def test_pitchtools_PitchRange___ge___02():

    pitch_range = pitchtools.PitchRange.from_pitches(-39, 48)

    assert NamedPitch(-99) <= pitch_range
    assert NamedPitch(-39) <= pitch_range
    assert not NamedPitch(0) <= pitch_range
    assert not NamedPitch(48) <= pitch_range
    assert not NamedPitch(99) <= pitch_range
