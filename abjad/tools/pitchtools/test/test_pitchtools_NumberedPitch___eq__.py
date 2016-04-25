# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch___eq___01():

    pitch_1 = pitchtools.NumberedPitch(12)
    pitch_2 = pitchtools.NumberedPitch(12)
    pitch_3 = pitchtools.NumberedPitch(13)

    assert pitch_1 == pitch_1
    assert pitch_1 == pitch_2
    assert not pitch_1 == pitch_3

    assert pitch_2 == pitch_1
    assert pitch_2 == pitch_2
    assert not pitch_2 == pitch_3

    assert not pitch_3 == pitch_1
    assert not pitch_3 == pitch_2
    assert pitch_3 == pitch_3
