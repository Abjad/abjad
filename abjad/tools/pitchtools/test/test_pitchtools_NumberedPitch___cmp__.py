# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch___cmp___01():

    pitch_1 = pitchtools.NumberedPitch(12)
    pitch_2 = pitchtools.NumberedPitch(12)

    assert not pitch_1 <  pitch_2
    assert      pitch_1 <= pitch_2
    assert      pitch_1 == pitch_2
    assert not pitch_1 != pitch_2
    assert not pitch_1 >  pitch_2
    assert      pitch_1 >= pitch_2


def test_pitchtools_NumberedPitch___cmp___02():

    pitch_1 = pitchtools.NumberedPitch(12)
    pitch_2 = pitchtools.NumberedPitch(13)

    assert not pitch_2 <  pitch_1
    assert not pitch_2 <= pitch_1
    assert not pitch_2 == pitch_1
    assert      pitch_2 != pitch_1
    assert      pitch_2 >  pitch_1
    assert      pitch_2 >= pitch_1


def test_pitchtools_NumberedPitch___cmp___03():

    pitch_1 = pitchtools.NumberedPitch(12)
    pitch_2 = 12

    assert not pitch_1 <  pitch_2
    assert      pitch_1 <= pitch_2
    assert      pitch_1 == pitch_2
    assert not pitch_1 != pitch_2
    assert not pitch_1 >  pitch_2
    assert      pitch_1 >= pitch_2


def test_pitchtools_NumberedPitch___cmp___04():

    pitch_1 = pitchtools.NumberedPitch(12)
    pitch_2 = 13

    assert not pitch_2 <  pitch_1
    assert not pitch_2 <= pitch_1
    assert not pitch_2 == pitch_1
    assert      pitch_2 != pitch_1
    assert      pitch_2 >  pitch_1
    assert      pitch_2 >= pitch_1
