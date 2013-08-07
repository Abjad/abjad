# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedChromaticPitch___eq___01():

    p = pitchtools.NumberedChromaticPitch(12)
    q = pitchtools.NumberedChromaticPitch(12)
    pitch_3 = pitchtools.NumberedChromaticPitch(13)

    assert p == p
    assert p == q
    assert not p == pitch_3

    assert q == p
    assert q == q
    assert not q == pitch_3

    assert not pitch_3 == p
    assert not pitch_3 == q
    assert pitch_3 == pitch_3
