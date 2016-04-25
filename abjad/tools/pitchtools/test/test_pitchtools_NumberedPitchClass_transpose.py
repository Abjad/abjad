# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitchClass_transpose_01():

    pc = pitchtools.NumberedPitchClass(1)
    assert pc.transpose(0) == pitchtools.NumberedPitchClass(1)
    assert pc.transpose(1) == pitchtools.NumberedPitchClass(2)
    assert pc.transpose(-1) == pitchtools.NumberedPitchClass(0)
    assert pc.transpose(99) == pitchtools.NumberedPitchClass(4)
    assert pc.transpose(-99) == pitchtools.NumberedPitchClass(10)
