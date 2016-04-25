# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSet___eq___01():
    r'''Pitch set equality works as expected.
    '''

    pitch_set_1 = pitchtools.PitchSet([12, 14, 18, 19])
    pitch_set_2 = pitchtools.PitchSet([12, 14, 18, 19])
    pitch_set_3 = pitchtools.PitchSet([12, 14, 18, 20])

    assert pitch_set_1 == pitch_set_2
    assert pitch_set_1 != pitch_set_3
    assert pitch_set_2 != pitch_set_3
    assert not pitch_set_1 != pitch_set_2
