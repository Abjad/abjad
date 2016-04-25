# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSet___contains___01():
    r'''Pitch set containment works as expected.
    '''

    pitch_set = pitchtools.PitchSet([12, 14, 18, 19])

    assert NamedPitch(14) in pitch_set
    assert NamedPitch(15) not in pitch_set
