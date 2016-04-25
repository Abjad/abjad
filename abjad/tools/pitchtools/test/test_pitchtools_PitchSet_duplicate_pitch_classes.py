# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSet_duplicate_pitch_classes_01():

    pitch_set = pitchtools.PitchSet([0, 12, 13, 26])

    assert pitch_set.duplicate_pitch_classes == pitchtools.PitchClassSet([0])


def test_pitchtools_PitchSet_duplicate_pitch_classes_02():

    pitch_set = pitchtools.PitchSet([0, 13, 26])

    assert pitch_set.duplicate_pitch_classes == pitchtools.PitchClassSet([])
