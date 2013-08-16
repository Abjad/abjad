# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedChromaticPitch___add___01():
    r'''Add numbered chromatic pitch to numbered chromatic pitch.
    '''

    pitch_1 = pitchtools.NumberedChromaticPitch(12)
    pitch_2 = pitchtools.NumberedChromaticPitch(13)

    assert pitch_1 + pitch_2 == pitchtools.NumberedChromaticPitch(25)


def test_NumberedChromaticPitch___add___02():
    r'''Add number to numbered chromatic pitch.
    '''

    pitch_1 = pitchtools.NumberedChromaticPitch(12)

    assert pitch_1 + 13 == pitchtools.NumberedChromaticPitch(25)
