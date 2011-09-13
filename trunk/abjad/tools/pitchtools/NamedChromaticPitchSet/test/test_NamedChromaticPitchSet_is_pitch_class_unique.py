from abjad import *


def test_NamedChromaticPitchSet_is_pitch_class_unique_01():

    pset = pitchtools.NamedChromaticPitchSet([0, 13, 26])
    assert pset.is_pitch_class_unique


def test_NamedChromaticPitchSet_is_pitch_class_unique_02():

    pset = pitchtools.NamedChromaticPitchSet([0, 12, 13, 26])
    assert not pset.is_pitch_class_unique


def test_NamedChromaticPitchSet_is_pitch_class_unique_03():
    '''Empty pitch-set and length-1 pitch-set boundary cases.'''

    assert pitchtools.NamedChromaticPitchSet([]).is_pitch_class_unique
    assert pitchtools.NamedChromaticPitchSet([13]).is_pitch_class_unique
