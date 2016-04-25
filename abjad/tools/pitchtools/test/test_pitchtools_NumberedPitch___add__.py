# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch___add___01():
    r'''Add numbered pitch to numbered pitch.
    '''

    pitch_1 = pitchtools.NumberedPitch(12)
    pitch_2 = pitchtools.NumberedPitch(13)

    assert pitch_1 + pitch_2 == pitchtools.NumberedPitch(25)


def test_pitchtools_NumberedPitch___add___02():
    r'''Add number to numbered pitch.
    '''

    pitch_1 = pitchtools.NumberedPitch(12)

    assert pitch_1 + 13 == pitchtools.NumberedPitch(25)
