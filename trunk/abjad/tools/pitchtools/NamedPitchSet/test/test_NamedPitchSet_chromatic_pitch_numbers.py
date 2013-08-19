# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitchSet_chromatic_pitch_numbers_01():
    r'''Works with multi-pitch pitch sets.
    '''

    pitch_set = pitchtools.NamedPitchSet([-10, 2, 9, 11])
    assert pitch_set.chromatic_pitch_numbers == (-10, 2, 9, 11)


def test_NamedPitchSet_chromatic_pitch_numbers_02():
    r'''Works with other pitch sets.
    '''

    pitch_set = pitchtools.NamedPitchSet([])
    assert pitch_set.chromatic_pitch_numbers == ()

    pitch_set = pitchtools.NamedPitchSet([-10])
    assert pitch_set.chromatic_pitch_numbers == (-10, )
