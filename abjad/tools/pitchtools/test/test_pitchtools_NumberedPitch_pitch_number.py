# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch_pitch_number_01():

    assert pitchtools.NumberedPitch("cff''").pitch_number == 10
    assert pitchtools.NumberedPitch("ctqf''").pitch_number == 10.5
    assert pitchtools.NumberedPitch("cf''").pitch_number == 11
    assert pitchtools.NumberedPitch("cqf''").pitch_number == 11.5
    assert pitchtools.NumberedPitch("c''").pitch_number == 12
    assert pitchtools.NumberedPitch("cqs''").pitch_number == 12.5
    assert pitchtools.NumberedPitch("cs''").pitch_number == 13
    assert pitchtools.NumberedPitch("ctqs''").pitch_number == 13.5
    assert pitchtools.NumberedPitch("css''").pitch_number == 14
    assert pitchtools.NumberedPitch("d''").pitch_number == 14
