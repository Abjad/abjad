# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch___init___01():
    r'''Initialize with number.
    '''

    assert isinstance(pitchtools.NumberedPitch(0), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(0.5), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(12), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(12.5), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(-12), pitchtools.NumberedPitch)
    assert isinstance(pitchtools.NumberedPitch(-12.5), pitchtools.NumberedPitch)


def test_pitchtools_NumberedPitch___init___02():
    r'''Initialize with other numbered pitch instance.
    '''

    numbered_pitch_1 = pitchtools.NumberedPitch(13)
    numbered_pitch_2 = pitchtools.NumberedPitch(numbered_pitch_1)

    assert isinstance(numbered_pitch_1, pitchtools.NumberedPitch)
    assert isinstance(numbered_pitch_2, pitchtools.NumberedPitch)
