# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedChromaticPitch___sub___01():
    r'''Subtract numbered chromatic pitch from numbered chromatic pitch.
    '''

    pitch_1 = pitchtools.NumberedChromaticPitch(12)
    pitch_2 = pitchtools.NumberedChromaticPitch(13)

    assert pitch_1 - pitch_2 == pitchtools.NumberedChromaticPitch(-1)
    assert pitch_2 - pitch_1 == pitchtools.NumberedChromaticPitch(1)


def test_NumberedChromaticPitch___sub___02():
    r'''Subtract number from numbered chromatic pitch.
    '''

    pitch_1 = pitchtools.NumberedChromaticPitch(12)

    assert pitch_1 - 13 == pitchtools.NumberedChromaticPitch(-1)
