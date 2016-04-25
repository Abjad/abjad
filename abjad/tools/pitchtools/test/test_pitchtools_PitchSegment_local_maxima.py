# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSegment_local_maxima_01():

    pitch_segment = pitchtools.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
    assert pitch_segment.local_maxima == (NamedPitch(7), )
