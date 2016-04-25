# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSet_is_pitch_class_unique_01():

    pitch_set = pitchtools.PitchSet([0, 13, 26])
    assert pitch_set.is_pitch_class_unique


def test_pitchtools_PitchSet_is_pitch_class_unique_02():

    pitch_set = pitchtools.PitchSet([0, 12, 13, 26])
    assert not pitch_set.is_pitch_class_unique


def test_pitchtools_PitchSet_is_pitch_class_unique_03():
    r'''Empty pitch-set and length-1 pitch-set boundary cases.
    '''

    assert pitchtools.PitchSet([]).is_pitch_class_unique
    assert pitchtools.PitchSet([13]).is_pitch_class_unique
