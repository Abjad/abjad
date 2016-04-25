# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange_one_line_numbered_pitch_repr_01():

    pitch_range = pitchtools.PitchRange.from_pitches(-12, 36)
    assert pitch_range.one_line_numbered_pitch_repr == '[-12, 36]'
