# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitchClass_multiply_01():

    assert pitchtools.NumberedPitchClass(0).multiply(5) == pitchtools.NumberedPitchClass(0)
    assert pitchtools.NumberedPitchClass(1).multiply(5) == pitchtools.NumberedPitchClass(5)
    assert pitchtools.NumberedPitchClass(2).multiply(5) == pitchtools.NumberedPitchClass(10)
    assert pitchtools.NumberedPitchClass(3).multiply(5) == pitchtools.NumberedPitchClass(3)
    assert pitchtools.NumberedPitchClass(4).multiply(5) == pitchtools.NumberedPitchClass(8)
    assert pitchtools.NumberedPitchClass(5).multiply(5) == pitchtools.NumberedPitchClass(1)
    assert pitchtools.NumberedPitchClass(6).multiply(5) == pitchtools.NumberedPitchClass(6)
    assert pitchtools.NumberedPitchClass(7).multiply(5) == pitchtools.NumberedPitchClass(11)
    assert pitchtools.NumberedPitchClass(8).multiply(5) == pitchtools.NumberedPitchClass(4)
    assert pitchtools.NumberedPitchClass(9).multiply(5) == pitchtools.NumberedPitchClass(9)
    assert pitchtools.NumberedPitchClass(10).multiply(5) == pitchtools.NumberedPitchClass(2)
    assert pitchtools.NumberedPitchClass(11).multiply(5) == pitchtools.NumberedPitchClass(7)
