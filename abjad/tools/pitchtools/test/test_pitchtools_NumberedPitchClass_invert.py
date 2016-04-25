# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitchClass_invert_01():

    assert pitchtools.NumberedPitchClass(0).invert() == pitchtools.NumberedPitchClass(0)
    assert pitchtools.NumberedPitchClass(1).invert() == pitchtools.NumberedPitchClass(11)
    assert pitchtools.NumberedPitchClass(2).invert() == pitchtools.NumberedPitchClass(10)
    assert pitchtools.NumberedPitchClass(3).invert() == pitchtools.NumberedPitchClass(9)
    assert pitchtools.NumberedPitchClass(4).invert() == pitchtools.NumberedPitchClass(8)
    assert pitchtools.NumberedPitchClass(5).invert() == pitchtools.NumberedPitchClass(7)
    assert pitchtools.NumberedPitchClass(6).invert() == pitchtools.NumberedPitchClass(6)
    assert pitchtools.NumberedPitchClass(7).invert() == pitchtools.NumberedPitchClass(5)
    assert pitchtools.NumberedPitchClass(8).invert() == pitchtools.NumberedPitchClass(4)
    assert pitchtools.NumberedPitchClass(9).invert() == pitchtools.NumberedPitchClass(3)
    assert pitchtools.NumberedPitchClass(10).invert() == pitchtools.NumberedPitchClass(2)
    assert pitchtools.NumberedPitchClass(11).invert() == pitchtools.NumberedPitchClass(1)
