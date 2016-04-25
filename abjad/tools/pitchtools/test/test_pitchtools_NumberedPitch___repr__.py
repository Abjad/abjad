# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NumberedPitch


def test_pitchtools_NumberedPitch___repr___01():
    r'''Numbered pitch repr is evaluable.
    '''

    numbered_pitch_1 = pitchtools.NumberedPitch(13)
    numbered_pitch_2 = eval(repr(numbered_pitch_1))

    assert isinstance(numbered_pitch_1, pitchtools.NumberedPitch)
    assert isinstance(numbered_pitch_2, pitchtools.NumberedPitch)
