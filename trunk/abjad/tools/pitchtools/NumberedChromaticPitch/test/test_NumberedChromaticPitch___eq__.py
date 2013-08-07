# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedChromaticPitch___eq___01():

    pitch_1 = pitchtools.NumberedChromaticPitch(12)
    pitch_2 = pitchtools.NumberedChromaticPitch(12)
    pitch_3 = pitchtools.NumberedChromaticPitch(13)

    assert pitch_1 == pitch_1
    assert pitch_1 == pitch_2
    assert not pitch_1 == pitch_3

    assert pitch_2 == pitch_1
    assert pitch_2 == pitch_2
    assert not pitch_2 == pitch_3

    assert not pitch_3 == pitch_1
    assert not pitch_3 == pitch_2
    assert pitch_3 == pitch_3
