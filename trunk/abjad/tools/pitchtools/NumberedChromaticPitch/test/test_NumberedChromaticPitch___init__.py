# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedChromaticPitch___init___01():
    r'''Init with number.
    '''

    assert isinstance(pitchtools.NumberedChromaticPitch(0), pitchtools.NumberedChromaticPitch)
    assert isinstance(pitchtools.NumberedChromaticPitch(0.5), pitchtools.NumberedChromaticPitch)
    assert isinstance(pitchtools.NumberedChromaticPitch(12), pitchtools.NumberedChromaticPitch)
    assert isinstance(pitchtools.NumberedChromaticPitch(12.5), pitchtools.NumberedChromaticPitch)
    assert isinstance(pitchtools.NumberedChromaticPitch(-12), pitchtools.NumberedChromaticPitch)
    assert isinstance(pitchtools.NumberedChromaticPitch(-12.5), pitchtools.NumberedChromaticPitch)


def test_NumberedChromaticPitch___init___02():
    r'''Init with other numbered chromatic pitch instance.
    '''

    numbered_chromatic_pitch_1 = pitchtools.NumberedChromaticPitch(13)
    numbered_chromatic_pitch_2 = pitchtools.NumberedChromaticPitch(numbered_chromatic_pitch_1)

    assert isinstance(numbered_chromatic_pitch_1, pitchtools.NumberedChromaticPitch)
    assert isinstance(numbered_chromatic_pitch_2, pitchtools.NumberedChromaticPitch)
