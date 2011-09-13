from abjad import *


def test_NamedChromaticPitchSet_duplicate_pitch_classes_01():

    pset = pitchtools.NamedChromaticPitchSet([0, 12, 13, 26])

    assert pset.duplicate_pitch_classes == pitchtools.NumberedChromaticPitchClassSet([0])


def test_NamedChromaticPitchSet_duplicate_pitch_classes_02():

    pset = pitchtools.NamedChromaticPitchSet([0, 13, 26])

    assert pset.duplicate_pitch_classes == pitchtools.NumberedChromaticPitchClassSet([])
