# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitch___float___01():
    r'''Returns pitch number of 12-ET numbered pitch as float.
    '''

    numbered_pitch = pitchtools.NumberedPitch(13)
    assert isinstance(float(numbered_pitch), float)
    assert float(numbered_pitch) == 13.0


def test_pitchtools_NumberedPitch___float___02():
    r'''Returns pitch number of 24-ET numbered pitch as float.
    '''

    numbered_pitch = pitchtools.NumberedPitch(13.5)
    assert isinstance(float(numbered_pitch), float)
    assert float(numbered_pitch) == 13.5
