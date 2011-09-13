from abjad import *


def test_NumberedChromaticPitchClassSet_numbered_chromatic_pitch_classes_01():

    pcset = pitchtools.NumberedChromaticPitchClassSet([0, 6, 10, 4, 9, 2])
    numbered_chromatic_pitch_classes = pcset.numbered_chromatic_pitch_classes

    assert isinstance(numbered_chromatic_pitch_classes, tuple)

    assert numbered_chromatic_pitch_classes[0] == 0
    assert numbered_chromatic_pitch_classes[1] == 2
    assert numbered_chromatic_pitch_classes[2] == 4
    assert numbered_chromatic_pitch_classes[3] == 6
    assert numbered_chromatic_pitch_classes[4] == 9
    assert numbered_chromatic_pitch_classes[5] == 10
