from abjad import *


def test_NamedChromaticPitchSet_numbered_chromatic_pitch_class_set_01():

    pset = pitchtools.NamedChromaticPitchSet([0, 13, 26])
    pcset = pitchtools.NumberedChromaticPitchClassSet([0, 1, 2])

    assert pset.numbered_chromatic_pitch_class_set == \
        pitchtools.NumberedChromaticPitchClassSet([0, 1, 2])
