# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch_transpose_01():

    assert pitchtools.NumberedPitch(12).transpose(6) == 18
    assert pitchtools.NumberedPitch(12).transpose(-6) == 6
    assert pitchtools.NumberedPitch(12).transpose(0) == 12
    assert pitchtools.NumberedPitch(12).transpose(0.5) == 12.5
