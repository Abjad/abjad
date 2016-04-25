# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSegment___max___01():

    pitch_segment = pitchtools.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
    assert max(pitch_segment) == NamedPitch(7)
