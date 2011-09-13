from abjad import *


def test_NamedChromaticPitchSet_chromatic_pitch_numbers_01():
    '''Works with multi-pitch pitch sets.'''

    pitch_set = pitchtools.NamedChromaticPitchSet([-10, 2, 9, 11])
    assert pitch_set.chromatic_pitch_numbers == (-10, 2, 9, 11)


def test_NamedChromaticPitchSet_chromatic_pitch_numbers_02():
    '''Works with other pitch sets.'''

    pitch_set = pitchtools.NamedChromaticPitchSet([])
    assert pitch_set.chromatic_pitch_numbers == ()

    pitch_set = pitchtools.NamedChromaticPitchSet([-10])
    assert pitch_set.chromatic_pitch_numbers == (-10, )
