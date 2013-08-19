# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitch___float___01():
    r'''Return chromatic pitch number of 12-ET numbered chromatic pitch as float.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedPitch(13)
    assert isinstance(float(numbered_chromatic_pitch), float)
    assert float(numbered_chromatic_pitch) == 13.0


def test_NumberedPitch___float___02():
    r'''Return chromatic pitch number of 24-ET numbered chromatic pitch as float.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedPitch(13.5)
    assert isinstance(float(numbered_chromatic_pitch), float)
    assert float(numbered_chromatic_pitch) == 13.5
